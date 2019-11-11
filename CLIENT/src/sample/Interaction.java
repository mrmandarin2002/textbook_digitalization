package sample;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

class Interaction {

    private DatagramSocket socket;
    private InetAddress server_address;
    private int server_port;

    private byte[] buf;

    public Interaction(String server_a, int server_p) throws SocketException, UnknownHostException {
        socket = new DatagramSocket();
        server_address = InetAddress.getByName(server_a);
        server_port = server_p;
    }

    public String client_echo(String msg) throws IOException {
        // convert message argument into byte-array form
        buf = msg.getBytes();
        
        // form and send message datagram
        DatagramPacket packet = new DatagramPacket(buf, buf.length, server_address, server_port);
        socket.send(packet);

        // form and receive response datagram
        packet = new DatagramPacket(buf, buf.length);
        socket.receive(packet);

        // process and return received data
        String received = new String(packet.getData(), 0, packet.getLength());
        return received;
    }

    public String client_command(String cmd, String[] args) throws IOException {
        String msg = cmd+";"+args[0];
        for (int i = 1; i < args.length; i++) {
            msg += ","+args[i];
        }
        System.out.println(msg);
        return client_echo(msg);
    }

    public void close() {
        socket.close();
    }

}