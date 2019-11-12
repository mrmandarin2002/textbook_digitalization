package sample;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

class Interaction {

    // define socket object, server address, and destination port
    private DatagramSocket socket;
    private InetAddress server_address;
    private int server_port;

    // create byte-type array for datagram buffer
    private byte[] buf;

    // Interaction object initialization method
    public Interaction(String server_a, int server_p) throws SocketException, UnknownHostException {
        // create new datagram socket (udp socket) object
        socket = new DatagramSocket();
        // assign server address to InetAddress object derived from server address
        server_address = InetAddress.getByName(server_a);
        // assign private server port variable to server port
        server_port = server_p;
        // set socket listener timeout to 1 second
        socket.setSoTimeout(1000);
    }

    // basic echo method
    // sends a string to the server and returns the response if/when it arrives
    public String client_echo(String msg) throws IOException {
        // convert message argument into byte-array form
        buf = msg.getBytes();
        
        // form and send message datagram
        DatagramPacket packet = new DatagramPacket(buf, buf.length, server_address, server_port);
        socket.send(packet);

        // form response datagram
        packet = new DatagramPacket(buf, buf.length);
        
        try {
            // receive, process, and return response data
            socket.receive(packet);
            String received = new String(packet.getData(), 0, packet.getLength());
            return received;
        } catch (Exception e) { // if the socket timeout exception was thrown, simply return 0
            return "0";
        }
    }

    // send a formatted command and arguments to the server and return the response
    public String client_command(String cmd, String[] args) throws IOException {
        // only loop through the arguments array if there is at least one argument
        if (args.length > 0) {
            // create initial message string, including the first element of the arguments array
            String msg = cmd+";"+args[0];
            // add remaining elements of the arguments array
            for (int i = 1; i < args.length; i++) {
                msg += ","+args[i]; // concatenate ith element of the arguments array
            }
            // return the response of the fully formed message string
            return client_echo(msg);
        } else {
            // return the response of the command
            return client_echo(cmd+";");
        }
    }

    // ping method
    // returns true if the server response arrives within less than 1 second, returns false otherwise
    public Boolean ping() throws IOException {
        // create an empty arguments array
        String[] a = {};
        // check if the response from the server is "1"
        if (client_command("p", a).equals("1")) {
            return true;
        } else {
            return false;
        }
    }

    // method to close the udp socket
    public void close() {
        socket.close();
    }

}