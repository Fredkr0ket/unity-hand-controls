using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        try
        {
            // Create a new TCP/IP socket.
            Socket listener = new Socket(AddressFamily.InterNetwork,
                SocketType.Stream, ProtocolType.Tcp);

            // Bind the socket to the local endpoint and listen for incoming connections.
            IPAddress ipAddress = IPAddress.Parse("127.0.0.1");
            IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 5005);
            listener.Bind(localEndPoint);
            listener.Listen(10);

            Console.WriteLine("Waiting for a connection on port 5005...");

            while (true)
            {
                // Wait for a connection and accept it.
                Socket handler = listener.Accept();

                // Receive the data from the client.
                byte[] buffer = new byte[1024];
                string data = null;
                while (true)
                {
                    int bytesReceived = handler.Receive(buffer);
                    data += Encoding.ASCII.GetString(buffer, 0, bytesReceived);
                    if (data.IndexOf("<EOF>") > -1)
                    {
                        break;
                    }
                }

                // Show the data on the console.
                Console.WriteLine("Received: {0}", data);

                // Echo the data back to the client.
                byte[] message = Encoding.ASCII.GetBytes(data);
                handler.Send(message);

                // Release the socket.
                handler.Shutdown(SocketShutdown.Both);
                handler.Close();
            }

        }
        catch (Exception e)
        {
            Console.WriteLine(e.ToString());
        }

        Console.WriteLine("\nPress any key to continue...");
        Console.ReadKey();
    }
}
