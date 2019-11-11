package sample;

import sample.Interaction;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

class interaction_test {
    public static void main(String[] args) throws SocketException, UnknownHostException, IOException{
        Interaction client = new Interaction("127.0.0.1", 7356);
        String arguments[] = {"a", "b", "C"};
        System.out.println(client.client_command("p", arguments));
        client.close();
    }
}