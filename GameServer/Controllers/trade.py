#!/usr/bin/env python3
__author__      = "Icseon"
__copyright__   = "Copyright (C) 2021 Icseon"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character

'''
This method will send a trade request to a remote client (if possible).
Additionally, a temporary trade_request session is created to validate the existence of a request.
'''
def trade_request(**_args):

    # Read local and remote character name from request
    local_character  = _args['packet'].ReadString(2)
    remote_character = _args['packet'].ReadString().strip()

    # Construct local error packet, in case the remote client is unable to trade
    error = PacketWrite()
    error.AddHeader(bytes=[0x39, 0x2F])
    error.AppendBytes(bytes=[0x00, 0x00])

    # Attempt to find the remote client, if it was not found then return an error
    # If the remove client is our client, send an error as well.
    # Lastly, a trade request should fail if the remote client is in a room or in a trade.
    remote_client = _args['connection_handler'].GetCharacterClient(remote_character)
    if remote_client is None \
            or remote_client is _args['client'] \
            or 'room' in remote_client \
            or 'trade_session' in remote_client:
        return _args['socket'].send(error.packet)

    '''
    Create trade request session that automatically expires after 12 seconds
    This is to ensure that a potential cheater can not create a trade session without the remote player's explicit
    approval.
    '''
    session = _args['session_handler'].create(
        type            = 'trade_request',
        clients         = [ remote_client ],
        data            = {'requester': _args['client']},
        expires_after   = 12
    )

    # Create trade request packet and send it to the remote client
    request = PacketWrite()
    request.AddHeader(bytes=[0x53, 0x2B])
    request.AppendBytes(bytes=[0x0C, 0x00])
    request.AppendString(_args['client']['character']['name'], 15)
    request.AppendString(remote_client['character']['name'], 15)
    _args['session_handler'].broadcast(session, request.packet)

'''
This method will parse the trade request response.
If accepted, a trade session will be created.
'''
def trade_request_response(**_args):

    # Read response, local and remote character names
    response            = int(_args['packet'].GetByte(0))
    local_character     = _args['packet'].ReadString(4)
    remote_character    = _args['packet'].ReadString().strip()

    # Attempt to find the request session
    request_session = None
    for session in _args['server'].sessions:

        # The session must be a trade request, our client must be in its client container
        # and the requesters character name has to be equal to the remove character name we received
        if session['type'] == 'trade_request' \
            and _args['client'] in session['clients'] \
                and session['data']['requester']['character']['name'] == remote_character:
            request_session = session

    # Create result packet
    result = PacketWrite()
    result.AddHeader(bytes=[0x39, 0x2F])

    # Check if we have found the session in question. Drop the packet and send an error if we did not.
    # If this is the case, we want to tell the client they refused the request no matter what.
    if request_session is None:
        result.AddHeader(bytes=[0x39, 0x2F]) # You have refused the trade request
        return _args['socket'].send(result.packet)

    # Destroy the session
    _args['session_handler'].destroy(session)

    # If the response is equal to 0 (refused), send the refused packet to both our own client and the remote client
    if response == 0:

        # Send refusal packet to our own client
        result.AppendBytes(bytes=[0x00, 0x01])  # You have refused the trade request
        _args['socket'].send(result.packet)

        # Construct new packet of refusal and send to the remote client
        remote_result = PacketWrite()
        remote_result.AddHeader(bytes=[0x28, 0x2F]) # For some reason T-Bot broke the regular trade denied packet
                                                    # so we're using the friend request response packet instead.
        remote_result.AppendBytes(bytes=[0x00, 0x1E])
        return session['data']['requester']['socket'].send(remote_result.packet)

    # Construct default item and currency pool
    pool_default    = {'items': [], 'currency_oil': 0, 'currency_gold': 0}
    state_default   = {'completed': False, 'approved': False}

    # Create trade session
    trade_session = _args['session_handler'].create(
        type='trade',
        clients=[
            _args['client'],
            session['data']['requester']
        ],
        data={
            'item_pool': {
                _args['client']['character']['id']:                pool_default.copy(),     # Our client's item pool
                session['data']['requester']['character']['id']:   pool_default.copy()      # Remote client's item pool
            },
            'states': {
                _args['client']['character']['id']: state_default.copy(),                    # Our client's state
                session['data']['requester']['character']['id']: state_default.copy()        # Remote client's state
            }
        }
    )

    # Assign session to clients
    for client in trade_session['clients']:
        client['trade_session'] = trade_session

    # Construct success packet and send the success packet to the remote client
    result.AppendBytes(bytes=[0x01, 0x00, 0x01, 0x00])
    result.AppendString(_args['client']['character']['name'], 15)
    result.AppendString(session['data']['requester']['character']['name'], 15)
    session['data']['requester']['socket'].send(result.packet)

'''
This method will retrieve the trade session from a specific given client.
If there is no session, False is returned
'''
def get_session(client):

    if 'trade_session' in client:
        return client['trade_session']

    return False

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
    character_name  = _args['packet'].ReadString()
    message         = _args['packet'].ReadStringByRange(21, (21 + 128))

    # Validate character name. Drop packet if it does not match our own.
    if character_name != _args['client']['character']['name']:
        return

    # Construct response packet and broadcast to chat session
    result = PacketWrite()
    result.AddHeader([0x37, 0x27])
    result.AppendString(_args['client']['character']['name'], 15)
    result.AppendBytes([0x00, 0x00, 0x00, 0x00, 0x37, 0x00])
    result.AppendString(message, 128)
    _args['session_handler'].broadcast(session, result.packet)

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
    result.AddHeader([0x34, 0x27])
    result.AppendString(_args['client']['character']['name'], 15)
    _args['session_handler'].broadcast(session, result.packet)

    # Ensure all clients are unlinked from the trade session
    for client in session['clients']:
        client.pop('trade_session')

    # Destroy the trade session
    _args['session_handler'].destroy(session)

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
    character_name = _args['packet'].ReadString(2)

    # Verify if the character name matches our own
    if character_name != _args['client']['character']['name']:
        return

    # Get local character ID
    local_character_id = _args['client']['character']['id']

    # If not yet completed, push items to pool
    if not session['data']['states'][local_character_id]['completed']:

        # Read item inventory slots from packet
        item_1_slot = int(_args['packet'].ReadInteger(19, 4, 'little'))
        item_2_slot = int(_args['packet'].ReadInteger(23, 4, 'little'))
        item_3_slot = int(_args['packet'].ReadInteger(27, 4, 'little'))

        # Construct item array, for use in validation and the item pool
        item_slots = []
        for slot in [item_1_slot, item_2_slot, item_3_slot]:

            # If the slot number is higher than 19 (actually 20, but 0 counts too), skip iteration.
            # The item was not provided in this case.
            if slot > 19:
                continue

            item_slots.append(slot)

        # Check against duplicate item slot numbers. We will be dropping the packet if a duplicate ia detected.
        if len(set(item_slots)) != len(item_slots):
            return

        # Retrieve our inventory
        inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')

        # Check if all slots are actually in the inventory.
        # Drop the packet if this is not the case.
        for slot in item_slots:
            if slot not in inventory:
                return

        # Retrieve our item pool and push the items and currency values to said pool
        pool            = session['data']['item_pool'][local_character_id]
        pool['items']   = item_slots

    # If completed, revert pool to default state
    else:
        session['data']['item_pool'][local_character_id] = {'items': [], 'currency_oil': 0, 'currency_gold': 0}

    # Mutate completed state, should be the opposite of the current state
    session['data']['states'][local_character_id]['completed'] = \
        not session['data']['states'][local_character_id]['completed']

    # Create pool sync packet, for each client in the container
    for client in session['clients']:

        # Construct result packet
        result = PacketWrite()
        result.AddHeader([0x35, 0x27])

        # Retrieve the inventory and pool in the scope of the current client
        local_inventory   = Character.get_items(_args, client['character']['id'], 'inventory')
        local_pool        = session['data']['item_pool'][client['character']['id']]

        # Retrieve the items from the inventory and add them to the packet
        for i in range(1, 4):

            # If the item wasn't found, append 9 null bytes (indicating that there is no item)
            if i > len(local_pool['items']) or local_pool['items'][i - 1] not in local_inventory:
                result.AppendBytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]) # No item
                continue

            # Retrieve item slot from the pool
            item_slot = local_pool['items'][i - 1]

            # Retrieve item from the inventory and add item to the packet
            result.AppendInteger(local_inventory[item_slot]['id'], 4, 'little')
            result.AppendInteger(local_inventory[item_slot]['duration'], 4, 'little')
            result.AppendInteger(local_inventory[item_slot]['duration_type'], 1, 'little')

        result.AppendInteger(1, 4, 'little') # Gold
        result.AppendInteger(2, 4, 'little') # Oil

        # Retrieve remote character ID
        remote_character_id = None
        for character_id in session['data']['item_pool'].keys():
            if int(character_id) != int(client['character']['id']):
                remote_character_id = character_id
                break

        # Retrieve remove inventory and item pool
        remote_inventory   = Character.get_items(_args, remote_character_id, 'inventory')
        remote_pool        = session['data']['item_pool'][remote_character_id]

        # Retrieve the items from the inventory and add them to the packet
        for i in range(1, 4):

            # If the item wasn't found, append 9 null bytes (indicating that there is no item)
            if i > len(remote_pool['items']) or remote_pool['items'][i - 1] not in remote_inventory:
                result.AppendBytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # No item
                continue

            # Retrieve item slot from the pool
            item_slot = remote_pool['items'][i - 1]

            # Retrieve item from the inventory and add item to the packet
            result.AppendInteger(remote_inventory[item_slot]['id'], 4, 'little')
            result.AppendInteger(remote_inventory[item_slot]['duration'], 4, 'little')
            result.AppendInteger(remote_inventory[item_slot]['duration_type'], 1, 'little')

        result.AppendInteger(3, 4, 'little')
        result.AppendInteger(4, 4, 'little')

        # Send result packet to the client
        client['socket'].send(result.packet)

        # Sync trade states between clients
        result = PacketWrite()
        result.AddHeader([0x36, 0x27])

        # Our local state
        result.AppendBytes([0x00 if not session['data']['states'][client['character']['id']]['completed'] else 0x01,
                            0x00 if not session['data']['states'][client['character']['id']]['approved'] else 0x01])

        # Remote state
        result.AppendBytes([0x00 if not session['data']['states'][remote_character_id]['completed'] else 0x01,
                            0x00 if not session['data']['states'][remote_character_id]['approved'] else 0x01])
        client['socket'].send(result.packet)