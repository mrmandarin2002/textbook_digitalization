package sample;

import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class interaction {

    // initialize client socket
    private DatagramSocket socket;
    private InetAddress address;

    private String server_address;
    private int server_port;

    private byte[] buf;

    public interaction(String server_a, int server_p) throws SocketException, UnknownHostException {
        server_address = server_a;
        server_port = server_p;
        socket = new DatagramSocket();
        address = InetAddress.getByName("localhost");
    }
    
    public String command(String cmd) {


        return "HELLO";
    }

    public void close() {
        socket.close();
    }
}