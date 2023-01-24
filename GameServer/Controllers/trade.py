#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2021 Icseon"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character

'''
This method will send a trade request to a remote client (if possible).
Additionally, a temporary trade_request session is created to validate the existence of a request.
'''


def trade_request(**_args):
    # Read local and remote character name from request
    _local_character = _args['packet'].read_string(2)
    remote_character = _args['packet'].read_string().strip()

    # Construct local error packet, in case the remote client is unable to trade
    error = PacketWrite()
    error.add_header(bytes=[0x39, 0x2F])
    error.append_bytes(bytes=[0x00, 0x00])

    # Attempt to find the remote client, if it was not found then return an error
    # If the remove client is our client, send an error as well.
    # Lastly, a trade request should fail if the remote client is in a room or in a trade.
    remote_client = _args['connection_handler'].get_character_client(remote_character)
    if remote_client is None \
            or remote_client is _args['client'] \
            or 'room' in remote_client \
            or 'trade_session' in remote_client:
        return _args['socket'].sendall(error.packet)

    '''
    Create trade request session that automatically expires after 12 seconds
    This is to ensure that a potential cheater can not create a trade session without the remote player's explicit
    approval.
    '''
    session = _args['session_handler'].create(
        type='trade_request',
        clients=[remote_client],
        data={'requester': _args['client']},
        expires_after=12
    )

    # This packet is sent to prevent a debugging error
    request = PacketWrite()
    request.add_header(bytes=[0x39, 0x2F])
    request.append_bytes(bytes=[0x00, 0x04])
    _args['session_handler'].broadcast(session, request.packet)

    # Create trade request packet and send it to the remote client
    request = PacketWrite()
    request.add_header(bytes=[0x53, 0x2B])
    request.append_bytes(bytes=[0x0C, 0x00])
    request.append_string(_args['client']['character']['name'], 15)
    # request.append_string(remote_client['character']['name'], 15)
    _args['session_handler'].broadcast(session, request.packet)


'''
This method will parse the trade request response.
If accepted, a trade session will be created.
'''


def trade_request_response(**_args):
    # Read response, local and remote character names
    response = int(_args['packet'].get_byte(0))
    _local_character = _args['packet'].read_string(4)
    remote_character = _args['packet'].read_string().strip()

    # Attempt to find the request session
    request_session = None
    for session in _args['server'].sessions:

        # The session must be a trade request, our client must be in its client container
        # and the requesters character name has to be equal to the remove character name we received
        if session['type'] == 'trade_request' \
                and _args['client'] in session['clients'] \
                and session['data']['requester']['character']['name'] == remote_character:
            request_session = session
            break

    # Create result packet
    result = PacketWrite()
    result.add_header(bytes=[0x39, 0x2F])

    # Check if we have found the session in question. Drop the packet and send an error if we did not.
    # If this is the case, we want to tell the client they refused the request no matter what.
    if request_session is None:
        result.add_header(bytes=[0x39, 0x2F])  # You have refused the trade request
        return _args['socket'].sendall(result.packet)

    # Destroy the session
    _args['session_handler'].destroy(request_session)

    # If the response is equal to 0 (refused), send the refused packet to both our own client and the remote client
    if response == 0:

        # Send refusal packet to our own client
        result.append_bytes(bytes=[0x00, 0x01])  # You have refused the trade request
        _args['socket'].sendall(result.packet)

        # Construct new packet of refusal and send to the remote client
        remote_result = PacketWrite()
        remote_result.add_header(bytes=[0x28, 0x2F])  # For some reason T-Bot broke the regular trade denied packet
        # so we're using the friend request response packet instead.
        remote_result.append_bytes(bytes=[0x00, 0x1E])
        try:
            request_session['data']['requester']['socket'].sendall(remote_result.packet)
        except Exception as e:
            print('Failed to send trade request denied packet to remote client because: ', str(e))
        return

    # Construct default item and currency pool
    pool_default = {'items': [], 'currency_oil': 0, 'currency_gold': 0}
    state_default = {'completed': False, 'approved': False}

    # Create trade session
    trade_session = _args['session_handler'].create(
        type='trade',
        clients=[
            _args['client'],
            request_session['data']['requester']
        ],
        data={
            'item_pool': {
                _args['client']['character']['id']: pool_default.copy(),  # Our client's item pool

                # Remote client's item pool
                request_session['data']['requester']['character']['id']: pool_default.copy()
            },
            'states': {
                _args['client']['character']['id']: state_default.copy(),  # Our client's state
                request_session['data']['requester']['character']['id']: state_default.copy()  # Remote client's state
            }
        }
    )

    # Assign session to clients
    for client in trade_session['clients']:
        client['trade_session'] = trade_session

    # Construct success packet and send the success packet to the remote client
    result.append_bytes(bytes=[0x01, 0x00, 0x01, 0x00])
    result.append_string(_args['client']['character']['name'], 15)
    result.append_string(request_session['data']['requester']['character']['name'], 15)
    try:
        request_session['data']['requester']['socket'].sendall(result.packet)
    except Exception as e:
        print('Failed to send trade initialization packet to remove client because: ', str(e))


'''
This method will retrieve the trade session from a specific given client.
If there is no session, False is returned
'''


def get_session(client):
    if 'trade_session' in client:
        return client['trade_session']

    return False


'''
This method will send a chat message in the trade chat
'''


def send_chat_message(_args, session, name, message):
    # Construct response packet and broadcast to chat session
    result = PacketWrite()
    result.add_header([0x37, 0x27])
    result.append_string(name, 15)
    result.append_bytes([0x00, 0x00, 0x00, 0x00, 0x37, 0x00])
    result.append_string(message, 128)
    _args['session_handler'].broadcast(session, result.packet)


'''
This method will handle trade chats by retrieving the message and then broadcasting it to the session
'''


def chat(**_args):
    """
    Check if our client is in a trade session before we proceed. We'll also be retrieving the session.
    """
    session = get_session(_args['client'])
    if not session:
        return

    # Read local character name and message
    character_name = _args['packet'].read_string()
    message = _args['packet'].read_string_by_range(21, (21 + 128))

    # Validate character name. Drop packet if it does not match our own.
    if character_name != _args['client']['character']['name']:
        return

    # Construct response packet and broadcast to chat session
    send_chat_message(_args=_args,
                      session=session,
                      name=_args['client']['character']['name'],
                      message=message)


'''
This method ls linked to the trade exit functionality and is invoked directly from a packet
Reason we have to do this is because we want to use the trade exit function outside of packet handling
'''


def exit_rpc(**_args):
    exit(_args)


'''
This method will allow users to exit trades at any moment and will end the trade session.
'''


def exit(_args):
    """
    Check if our client is in a trade session before proceeding.
    """
    session = get_session(_args['client'])
    if not session:
        return

    # Construct trade end packet and send to all clients in the trade session
    result = PacketWrite()
    result.add_header([0x34, 0x27])
    result.append_string(_args['client']['character']['name'], 15)
    _args['session_handler'].broadcast(session, result.packet)

    # Ensure all clients are unlinked from the trade session
    for client in session['clients']:
        client.pop('trade_session')

    # Destroy the trade session
    _args['session_handler'].destroy(session)


'''
This method obtains the remove character ID and returns it to the stack
'''


def get_remote_character_id(client, session):
    # Initialize result
    remote_character_id = None

    # Retrieve all character IDs by looking at the item pool keys (they are indexed by character IDs)
    for character_id in session['data']['item_pool'].keys():

        # Retrieve the first ID that is not ours and use that
        if int(character_id) != int(client['character']['id']):
            remote_character_id = character_id
            break

    return remote_character_id


'''
This method sends the acceptance and completion state to all clients and syncs the state
'''


def sync_state(session):
    for client in session['clients']:

        # Retrieve remote character ID to obtain remote client's state
        remote_character_id = get_remote_character_id(client, session)

        # Construct state packet
        result = PacketWrite()
        result.add_header([0x36, 0x27])

        # Add local state to the packet
        result.append_bytes([0x00 if not session['data']['states'][client['character']['id']]['completed'] else 0x01,
                             0x00 if not session['data']['states'][client['character']['id']]['approved'] else 0x01])

        # Add remote state to the packet
        result.append_bytes([0x00 if not session['data']['states'][remote_character_id]['completed'] else 0x01,
                             0x00 if not session['data']['states'][remote_character_id]['approved'] else 0x01])

        # Send state to the client
        try:
            client['socket'].sendall(result.packet)
        except Exception as e:
            print('Failed to send sync_state() result to client because: ', str(e))


'''
This method will let users confirm their choices and notify the opposite client of their choice
'''


def confirm_trade(**_args):
    """
    Check if our client is in a trade session before proceeding.
    """
    session = get_session(_args['client'])
    if not session:
        return

    # Read character name
    character_name = _args['packet'].read_string(2)

    # Verify if the character name matches our own
    if character_name != _args['client']['character']['name']:
        return

    # Get local character ID
    local_character_id = _args['client']['character']['id']

    # If not yet completed, push items to pool
    if not session['data']['states'][local_character_id]['completed']:

        # Read item inventory slots from packet
        item_1_slot = int(_args['packet'].read_integer(18, 4, 'little'))
        item_2_slot = int(_args['packet'].read_integer(22, 4, 'little'))
        item_3_slot = int(_args['packet'].read_integer(26, 4, 'little'))

        # Read currency amounts from packet
        currency_gold = int(_args['packet'].read_integer(30, 4, 'little'))
        currency_oil = int(_args['packet'].read_integer(34, 4, 'little'))

        # Overwrite currencies with zero in case they exceed the available amount
        if currency_gold > _args['client']['character']['currency_gigas']:
            currency_gold = 0

        if currency_oil > _args['client']['character']['currency_botstract']:
            currency_oil = 0

        # Construct item array, for use in validation and the item pool
        item_slots, validation_slots = [], []
        for slot in [item_1_slot, item_2_slot, item_3_slot]:

            # If the slot number is higher than 19 (aka none), append None else append the slot number
            slot_nr = None if slot > 19 else slot

            # Append slot to item slots and if it is not None, append to duplication check array
            item_slots.append(slot_nr)
            if slot_nr is not None:
                validation_slots.append(slot)

        # Check against duplicate item slot numbers. We will be dropping the packet if a duplicate is detected.
        if len(set(validation_slots)) != len(validation_slots):
            return

        # Retrieve our inventory
        inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')

        # Check if all slots are actually in the inventory.
        # Drop the packet if this is not the case.
        for slot in validation_slots:
            if slot not in inventory:
                return

        # Retrieve our item pool and push the items and currency values to said pool
        pool = session['data']['item_pool'][local_character_id]
        pool['items'] = item_slots
        pool['currency_gold'] = currency_gold
        pool['currency_oil'] = currency_oil

    # If completed, revert pool and status to default state
    else:
        session['data']['item_pool'][local_character_id] = {'items': [], 'currency_oil': 0, 'currency_gold': 0}

        # Make the approved state False for every client (all clients to prevent scamming)
        # Completed will be set shortly, if we do it here we cause a conflict
        for state in session['data']['states']:
            session['data']['states'][state]['approved'] = False

        # Construct and send item state reset packet
        result = PacketWrite()
        result.add_header([0x33, 0x27])
        for _ in range(100):
            result.append_bytes([0x00])
        _args['socket'].sendall(result.packet)

    # Mutate completed state, should be the opposite of the current state
    session['data']['states'][local_character_id]['completed'] = \
        not session['data']['states'][local_character_id]['completed']

    # Create pool sync packet, for each client in the container
    for client in session['clients']:

        # Construct result packet
        result = PacketWrite()
        result.add_header([0x35, 0x27])

        # Retrieve the inventory and pool in the scope of the current client
        local_inventory = Character.get_items(_args, client['character']['id'], 'inventory')
        local_pool = session['data']['item_pool'][client['character']['id']]

        # Retrieve the items from the inventory and add them to the packet
        for i in range(1, 4):

            # If the item wasn't found, append 9 null bytes (indicating that there is no item)
            if i > len(local_pool['items']) or local_pool['items'][i - 1] is None \
                    or local_pool['items'][i - 1] not in local_inventory:
                result.append_bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # No item
                continue

            # Retrieve item slot from the pool
            item_slot = local_pool['items'][i - 1]

            # Retrieve item from the inventory and add item to the packet
            result.append_integer(local_inventory[item_slot]['id'], 4, 'little')
            result.append_integer(local_inventory[item_slot]['duration'], 4, 'little')
            result.append_integer(local_inventory[item_slot]['duration_type'], 1, 'little')

        # Send local currencies to client
        result.append_integer(local_pool['currency_gold'], 4, 'little')
        result.append_integer(local_pool['currency_oil'], 4, 'little')

        # Retrieve remote character ID
        remote_character_id = get_remote_character_id(client, session)

        # Retrieve remove inventory and item pool
        remote_inventory = Character.get_items(_args, remote_character_id, 'inventory')
        remote_pool = session['data']['item_pool'][remote_character_id]

        # Retrieve the items from the inventory and add them to the packet
        for i in range(1, 4):

            # If the item wasn't found, append 9 null bytes (indicating that there is no item)
            if i > len(remote_pool['items']) or remote_pool['items'][i - 1] is None \
                    or remote_pool['items'][i - 1] not in remote_inventory:
                result.append_bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # No item
                continue

            # Retrieve item slot from the pool
            item_slot = remote_pool['items'][i - 1]

            # Retrieve item from the inventory and add item to the packet
            result.append_integer(remote_inventory[item_slot]['id'], 4, 'little')
            result.append_integer(remote_inventory[item_slot]['duration'], 4, 'little')
            result.append_integer(remote_inventory[item_slot]['duration_type'], 1, 'little')

        # Send remote currencies to client
        result.append_integer(remote_pool['currency_gold'], 4, 'little')
        result.append_integer(remote_pool['currency_oil'], 4, 'little')

        # Send result packet to the client
        try:
            client['socket'].sendall(result.packet)
        except Exception as e:
            print('Failed to send pool sync packet result to client because: ', str(e))

    # Sync trade state between clients
    sync_state(session)


'''
This method allows users to approve or decline the remote transaction / pool
'''


def approve_transaction(**_args):
    """
    Check if our client is in a trade session before proceeding.
    """
    session = get_session(_args['client'])
    if not session:
        return

    # If at least one client has not completed their item pool, drop the packet. Both clients need to be ready
    # in order to approve a transaction.
    for id in session['data']['states']:
        if not session['data']['states'][id]['completed']:
            return

    # Mutate accepted state. If it is True, become False and vise versa.
    session['data']['states'][_args['client']['character']['id']]['approved'] = \
        not session['data']['states'][_args['client']['character']['id']]['approved']

    # Sync state between the clients
    sync_state(session)

    # Check if all clients have approved the transaction
    for id in session['data']['states']:
        if not session['data']['states'][id]['approved']:
            return

    # We'll need a boolean because we want to be able to check more inventories at the same time
    inventory_validation_passed = True

    # For every client in the session, check if they have enough inventory slots available for their incoming pool
    for client in session['clients']:

        # Retrieve incoming pool, this will be used to see how many slots we require
        incoming_pool = session['data']['item_pool'][get_remote_character_id(client, session)]
        required_slots = len(
            [i for i in incoming_pool['items'] if i is not None])  # Calculate pool length, ignoring None instances

        # Retrieve our inventory
        inventory = Character.get_items(_args, client['character']['id'], 'inventory')

        # Calculate amount of available slots based on the inventory we just obtained
        # The local item pool size will also be available
        available_slots = len(
            [i for i in session['data']['item_pool'][client['character']['id']]['items'] if i is not None])
        for item in inventory:
            if inventory[item]['id'] == 0 and inventory[item]['character_item_id'] is None:
                available_slots += 1

        # If the required slots exceed the available slots, there is something wrong
        if required_slots > available_slots:
            send_chat_message(_args=_args,
                              session=session,
                              name='Server',
                              message="{0} does not have enough available inventory slots for this transaction. {1} "
                                      "slot(s) are available while {2} {3} required.".format(
                                        client['character']['name'],
                                        available_slots,
                                        required_slots,
                                        'is' if required_slots == 1 else 'are'))
            inventory_validation_passed = False

    # If the inventory validation failed for at least one client, do not proceed
    if not inventory_validation_passed:
        return

    # Array containing the transactions
    transactions = []

    # Construct transaction array from the perspective of all present clients
    for client in session['clients']:

        # Retrieve local pool and inventory
        pool = session['data']['item_pool'][client['character']['id']]
        inventory = Character.get_items(_args, client['character']['id'], 'inventory')

        # Construct item ID consisting of only character_item_id instances
        items = []
        for item in pool['items']:
            if item is not None:
                items.append(inventory[item]['character_item_id'])

        # Add to transactions array
        transactions.append({
            'to': get_remote_character_id(client, session),
            'items': items,
            'currencies': {
                'currency_gold': pool['currency_gold'],
                'currency_oil': pool['currency_oil']
            }
        })

        # If the currency_gold or currency_oil is greater than 0, update local state and character
        if pool['currency_gold'] > 0 or pool['currency_oil'] > 0:
            # Update local state
            client['character']['currency_gigas'] = (client['character']['currency_gigas'] - pool['currency_gold'])
            client['character']['currency_botstract'] = (
                    client['character']['currency_botstract'] - pool['currency_oil'])

            # Update character
            _args['mysql'].execute('''UPDATE `characters` SET
                    `currency_gigas`        = (`currency_gigas`     - %s),
                    `currency_botstract`    = (`currency_botstract` - %s)
                WHERE `id` = %s''', [
                pool['currency_gold'],
                pool['currency_oil'],
                client['character']['id']
            ])

    # Empty inventory based on the item pool
    for character_id in session['data']['item_pool'].keys():

        # Retrieve item pool slot numbers
        slot_numbers = session['data']['item_pool'][character_id]['items']

        # Construct SET statement
        set_statement = ''
        for number in slot_numbers:

            # Do not parse None items
            if number is None:
                continue

            set_statement += '`item_{0}` = 0, '.format(str(number + 1))

        # Perform inventory clean-up, but only if the set_statement is actually set
        if len(set_statement) > 0:
            _args['mysql'].execute(
                '''UPDATE `inventory` SET {0} WHERE `character_id` = %s'''.format(set_statement[:-2]), [
                    character_id
                ])

    # Reset item pools
    for pool in session['data']['item_pool']:
        session['data']['item_pool'][pool] = {'items': [], 'currency_oil': 0, 'currency_gold': 0}

    # Reset states
    for state in session['data']['states']:
        session['data']['states'][state]['completed'] = False
        session['data']['states'][state]['approved'] = False

    # Perform transactions
    for transaction in transactions:
        for item in transaction['items']:

            # Retrieve inventory and first available slot
            inventory = Character.get_items(_args, transaction['to'], 'inventory')
            available_slot = Character.get_available_inventory_slot(inventory)

            # Insert item in inventory
            if available_slot is not None:
                _args['mysql'].execute('''UPDATE `inventory` SET `item_{0}` = %s WHERE `character_id` = %s'''.format(
                    str(available_slot + 1)), [item, transaction['to']]
                )

        # Update character to accept the currency (if any)
        if transaction['currencies']['currency_gold'] > 0 or transaction['currencies']['currency_oil'] > 0:
            _args['mysql'].execute('''UPDATE `characters` SET
                                                            `currency_gigas`        = (`currency_gigas` + %s),
                                                            `currency_botstract`    = (`currency_botstract` + %s)
                WHERE `id` = %s''', [
                transaction['currencies']['currency_gold'],
                transaction['currencies']['currency_oil'],
                transaction['to']
            ])

            # Find target client and update currency states
            for client in session['clients']:
                if client['character']['id'] == transaction['to']:
                    client['character']['currency_gigas'] += transaction['currencies']['currency_gold']
                    client['character']['currency_botstract'] += transaction['currencies']['currency_oil']
                    break

    # Send inventory sync packet for every client in the session
    for client in session['clients']:

        # Construct inventory sync packet
        result = PacketWrite()
        result.add_header([0x33, 0x27])
        result.append_bytes([0x01, 0x00, 0x00, 0x00])

        # Retrieve inventory
        inventory = Character.get_items(_args, client['character']['id'], 'inventory')

        # Append inventory items to the packet
        for item in inventory:
            result.append_integer(inventory[item]['id'], 4, 'little')
            result.append_integer(inventory[item]['duration'], 4, 'little')
            result.append_integer(inventory[item]['duration_type'], 1, 'little')

        for _ in range(180):
            result.append_bytes([0x00])

        # Send currency amounts
        result.append_integer(client['character']['currency_gigas'], 4, 'little')
        result.append_integer(client['character']['currency_botstract'], 4, 'little')

        try:
            client['socket'].sendall(result.packet)
        except Exception as e:
            print('Failed to send inventory sync packet to client because: ', str(e))

    # Send transaction success message
    send_chat_message(_args=_args,
                      session=session,
                      name='Server',
                      message='Transaction successful!')
