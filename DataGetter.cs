using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program {
    static void Main() {
        // create a TCP/IP socket
        Socket listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        // bind the socket to the local endpoint
        IPAddress ipAddress = IPAddress.Parse("127.0.0.1");
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 5005);
        listener.Bind(localEndPoint);

        // start listening for incoming connections
        listener.Listen(1);

        Console.WriteLine("Waiting for a connection...");

        // accept a connection and receive data
        Socket handler = listener.Accept();
        byte[] buffer = new byte[1024];
        int bytesReceived = handler.Receive(buffer);
        string data = Encoding.ASCII.GetString(buffer, 0, bytesReceived);

        // print the received data to the console
        Console.WriteLine("Received: " + data);

        // clean up
        handler.Shutdown(SocketShutdown.Both);
        handler.Close();
    }
}