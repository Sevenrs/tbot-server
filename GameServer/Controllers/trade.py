#!/usr/bin/env python3
__author__      = "Icseon"
__copyright__   = "Copyright (C) 2021 Icseon"

from Packet.Write import Write as PacketWrite
import time

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
        clients         = [remote_client],
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

    # Create trade session
    trade_session = _args['session_handler'].create(
        type='trade',
        clients=[
            _args['client'],
            session['data']['requester']
        ]
    )

    # Assign session to clients
    for client in trade_session['clients']:
        client['trade_session'] = trade_session

    # Construct success packet and send the success packet to the remote client
    result.AppendBytes(bytes=[0x01, 0x00, 0x01, 0x00])
    result.AppendString(_args['client']['character']['name'], 15)
    result.AppendString(session['data']['requester']['character']['name'], 15)
    session['data']['requester']['socket'].send(result.packet)