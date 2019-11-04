public class interaction {

    // initialize client socket
    private DatagramSocket socket;
    private InetAddress address;

    public interaction() {
        socket = new DatagramSocket();
        address = InetAddress.getByName("localhost");
    }
    
    public static String command(String cmd) {

    }

    public void close() {
        socket.close();
    }
}