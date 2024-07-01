using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro; // Assuming TMP is used for UI elements
using UnityEngine.Networking; // Required for UnityWebRequest
public class GameManager : MonoBehaviour
{
    public TMP_InputField currentMessageInputField; // Assuming TMP_InputField is used
    public TMP_Text historicalMessagesText; // Assuming TMP_Text is used for TextMeshPro
    public Button sendButton;
    public ScrollRect scrollRect;
    public AudioSource responseAudioSource; // Reference to the AudioSource component
    public AudioClip audioClip; // Reference to the AudioClip you want to play
    public TCPConnectionHandler tcpConnectionHandler; // Reference to TCPConnectionHandler
    public AudioClip backgroundMusicClip; // New variable for background music
    public AudioSource backgroundAudioSource; // New AudioSource for response audio
    private List<string> historicalMessages = new List<string>();
    private const int maxMessages = 100; // Adjusted maxMessages to a reasonable number for demonstration

    void Start()
    {
        Debug.Log("GameManager started. Adding listener to send button.");
        sendButton.onClick.AddListener(parse_prompt);
        PlayBackgroundMusic(); 
    }
    void PlayBackgroundMusic()
    {
        if (backgroundAudioSource != null && backgroundMusicClip != null)
        {
            backgroundAudioSource.clip = backgroundMusicClip; // Set the background music clip
            backgroundAudioSource.loop = true; // Enable looping
            backgroundAudioSource.Play(); // Play the background music
        }
        else
        {
            Debug.LogError("AudioSource or backgroundMusicClip is missing.");
        }
    }
    
    void SendMessageToHistory(string currentMessage)
    {
            historicalMessages.Add(currentMessage);
            if (historicalMessages.Count > maxMessages)
            {
                Debug.Log("Maximum messages reached. Removing oldest message.");
                historicalMessages.RemoveAt(0); // Remove the oldest message if over cap
            }

            // Update the historical messages Text UI
            historicalMessagesText.text = string.Join("\n", historicalMessages.ToArray());

            // Clear the current message InputField
            currentMessageInputField.text = "";

            // Scroll to the bottom of the ScrollRect
            Canvas.ForceUpdateCanvases(); // Update Canvas immediately to correctly scroll
            scrollRect.verticalNormalizedPosition = 0;
    }
    void parse_prompt()
    {
        Debug.Log("Attempting to send message to history...");
        string currentMessage = currentMessageInputField.text;
        if (!string.IsNullOrWhiteSpace(currentMessage))
        {
            string mensaje_preparado = "TÚ: " + currentMessage + "\n";
            SendMessageToHistory(mensaje_preparado);
            Debug.Log($"Sending message: {currentMessage}");
            // Add the current message to the historical messages


            Debug.Log("Message sent and UI updated.");

            // Instead of directly activating other functions, send the message to the server and wait for a reply
            StartCoroutine(SendMessageToServerAndActivateFunctions(currentMessage));
        }
        else
        {
            Debug.Log("No message to send. Input field is empty or whitespace.");
        }
    }

    IEnumerator SendMessageToServerAndActivateFunctions(string message)
    {
        var sendMessageTask = tcpConnectionHandler.SendMessageAndWaitForReply(message);
        // Wait for the task to complete
        while (!sendMessageTask.IsCompleted)
        {
            //Debug.Log("Waiting for message to be sent and reply received...");
            yield return null; // Yield control back to the Unity engine until the next frame
        }
        Debug.Log("Message sent and reply received.");
        Debug.Log(sendMessageTask.Result);
        // Check if the task was faulted or canceled
        if (sendMessageTask.IsFaulted || sendMessageTask.IsCanceled)
        {
            // Log the exception if the task failed
            Debug.LogError($"Error sending message to server: {sendMessageTask.Exception?.GetBaseException().Message}");
        }
        else
        {
            string reply = sendMessageTask.Result; // Get the result of the task
            if (!string.IsNullOrEmpty(reply))
            {
                // Now that we have the reply, activate other functions
                ActivateOtherFunctions(reply);
            }
            else
            {
                Debug.LogError("No reply received from server or an error occurred.");
            }
        }
    }
    IEnumerator LoadAndPlayResponseAudio(string filePath)
    {
        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(filePath, AudioType.MPEG))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                if (responseAudioSource != null && clip != null)
                {
                    responseAudioSource.clip = clip;
                    Debug.Log("Playing response audio...");
                    responseAudioSource.Play();
                }
                else
                {
                    Debug.LogError("Response AudioSource or AudioClip is missing.");
                }
            }
            else
            {
                Debug.LogError($"Failed to load AudioClip from path: {filePath}");
            }
        }
    }
    void ActivateOtherFunctions(string reply)
    {
        string mensaje_preparado_ia = "ALINA: " + reply + "\n";
        SendMessageToHistory(mensaje_preparado_ia); // Add the server reply to the historical messages
        Debug.Log("Activating other functions...");

        // Specify the path to the MP3 file
        string mp3FilePath = Environment.GetEnvironmentVariable("VOLUMEN_AUDIO");

        // Load and play the audio
        StartCoroutine(LoadAndPlayResponseAudio(mp3FilePath));
    }
}