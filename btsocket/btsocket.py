# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import logging
import socket

import _btsocket
import constants

class BluetoothSocket(socket._socketobject):
    """Socket wrapper class for Bluetooth sockets.

    Wraps the Python socket class to implement the necessary pieces to be able
    to bind to the HCI monitor and control sockets as well as receive messages
    with ancillary data from them.

    """

    def __init__(self,
                 family=constants.AF_BLUETOOTH,
                 type=socket.SOCK_RAW,
                 proto=constants.BTPROTO_HCI):
        super(BluetoothSocket, self).__init__(family, type, proto)

    def bind(self, *args):
        """Bind the socket.

        For BTPROTO_HCI sockets args should be a tuple containing:

        @param dev device index to bind to, or HCI_DEV_NONE.
        @param channel channel to bind to, e.g. HCI_CHANNEL_RAW.

        """
        if self.family == constants.AF_BLUETOOTH:
            return _btsocket.bind(self, self.proto, *args)
        else:
            return super(BluetoothSocket, self).bind(*args)

    def recvmsg(self, bufsize, ancbufsize=0, flags=0):
        """Receive normal data and ancillary data from the socket.

        @param bufsize size in bytes of buffer for normal data.
        @param ancbufsize size in bytes of internal buffer for ancillary data.
        @param flags same meaning as socket.recv()

        @return tuple of (data, ancdata, msg_flags, address),
          @ancdata is zero or more tuples of (cmsg_level, cmsg_type, cmsg_data).

        """
        buffer = bytearray(bufsize)
        (nbytes, ancdata, msg_flags, address) = \
                self.recvmsg_into((buffer,), ancbufsize, flags)
        return (bytes(buffer), ancdata, msg_flags, address)

    def recvmsg_into(self, buffers, ancbufsize=0, flags=0):
        """Receive normal data and ancillary data from the socket.

        @param buffers iterable of bytearray objects filled with read chunks.
        @param ancbufsize size in bytes of internal buffer for ancillary data.
        @param flags same meaning as socket.recv()

        @return tuple of (nbytes, ancdata, msg_flags, address),
          @ancdata is zero or more tuples of (cmsg_level, cmsg_type, cmsg_data).

        """
        return _btsocket.recvmsg(self, buffers, ancbufsize, flags)

