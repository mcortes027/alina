using System;
using System.Collections;
using System.IO;
using System.Net.Sockets;
using System.Threading.Tasks;
using UnityEngine;

public class TCPConnectionHandler : MonoBehaviour
{
    private TcpClient tcpClient;
    private NetworkStream networkStream;
    private StreamReader streamReader;
    private StreamWriter streamWriter;
    public string serverIP = "127.0.0.1";
    public int serverPort = 8501;

    void Start()
    {
        ConnectToServer();
    }

    async void ConnectToServer()
    {
        try
        {
            tcpClient = new TcpClient();
            await tcpClient.ConnectAsync(serverIP, serverPort);
            Debug.Log("Connected to server");

            networkStream = tcpClient.GetStream();
            streamReader = new StreamReader(networkStream);
            streamWriter = new StreamWriter(networkStream) { AutoFlush = true };

            // Send an initial message
            //await SendMessageAsync("Hello from Unity!");

            //StartCoroutine(ListenForMessages());
        }
        catch (Exception e)
        {
            Debug.LogError($"Failed to connect to server: {e.Message}");
        }
    }

    IEnumerator ListenForMessages()
    {
        while (tcpClient != null && tcpClient.Connected)
        {
            if (networkStream.DataAvailable)
            {
                var readTask = ReadMessageAsync();
                yield return new WaitUntil(() => readTask.IsCompleted);

                if (readTask.Exception == null)
                {
                    var message = readTask.Result;
                    if (message != null)
                    {
                        Debug.Log($"Received from server: {message}");
                        // Execute any updates on the main thread here
                    }
                }
                else
                {
                    Debug.LogError($"Error reading message: {readTask.Exception.InnerException.Message}");
                    break; // Exit the loop in case of an error
                }
            }
            yield return null; // Wait for the next frame
        }
    }

    private Task<string> ReadMessageAsync()
    {
        return Task.Run(async () =>
        {
            try
            {
                Debug.Log("checking if streamReader is null.");
                if (streamReader == null)
                {
                    Debug.LogError("StreamReader is null.");
                    return null;
                }

                // Wait for data to become available
                Debug.Log("Waiting for data to become available...");
                while (!streamReader.EndOfStream)
                {
                    if (streamReader.Peek() >= 0)
                    {
                        Debug.Log("Reading message from server...");
                        return await streamReader.ReadLineAsync();
                    }
                    await Task.Delay(100); // Wait a bit before checking again to avoid a tight loop
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"Error reading message: {e.Message}");
            }
            return null;
        });
    }

    private async Task SendMessageAsync(string message)
    {
        if (streamWriter != null)
        {
            await streamWriter.WriteLineAsync(message);
        }
    }

    public async Task<string> SendMessageAndWaitForReply(string message)
    {
        try
        {
            Debug.Log($"Sending message to server: {message}");

            await SendMessageAsync(message);
            Debug.Log("Waiting for reply from server...");
            // Assuming the server sends a reply immediately after receiving a message
            return await ReadMessageAsync();
        }
        catch (Exception e)
        {
            Debug.LogError($"Error in SendMessageAndWaitForReply: {e.Message}");
            return null;
        }
    }

    void OnDestroy()
    {
        Disconnect();
    }

    private void Disconnect()
    {
        if (tcpClient != null)
        {
            if (tcpClient.Connected)
            {
                tcpClient.Close();
            }
            tcpClient = null;
            Debug.Log("Disconnected from server");
        }
    }
}