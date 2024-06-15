using System;
using System.IO;
using System.Net.Sockets;
using System.Threading.Tasks;
using UnityEngine;

public class TCPConnectionHandler : MonoBehaviour
{
    public string serverIP = "127.0.0.1";
    public int port = 11434;
    private TcpClient client;
    private StreamReader reader;

    public event Action<string> OnMessageReceived;

    void Start()
    {
        ConnectToServer();
    }

    async void ConnectToServer()
    {
        try
        {
            client = new TcpClient(serverIP, port);
            reader = new StreamReader(client.GetStream());
            Debug.Log("Connected to server.");
            await ReadMessages();
        }
        catch (Exception e)
        {
            Debug.LogError($"Failed to connect: {e.Message}");
        }
    }

    async Task ReadMessages()
    {
        string message = "";
        while ((message = await reader.ReadLineAsync()) != null)
        {
            OnMessageReceived?.Invoke(message);
        }
    }

    void OnDestroy()
    {
        reader?.Close();
        client?.Close();
    }
}