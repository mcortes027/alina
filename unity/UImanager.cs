using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    public TCPConnectionHandler tcpConnectionHandler;
    public InputField promptInputField;
    public Text historyText;

    void Start()
    {
        if (tcpConnectionHandler != null)
        {
            tcpConnectionHandler.OnMessageReceived += UpdateHistoryWithOllamaMessage;
        }
    }

    public void OnPromptSubmit()
    {
        string prompt = promptInputField.text;
        UpdateHistory(prompt, "Prompt");
        promptInputField.text = ""; // Clear the input field after submitting
    }

    void UpdateHistoryWithOllamaMessage(string message)
    {
        UpdateHistory(message, "Ollama");
    }

    void UpdateHistory(string message, string source)
    {
        historyText.text += $"\n{source}: {message}";
    }

    void OnDestroy()
    {
        if (tcpConnectionHandler != null)
        {
            tcpConnectionHandler.OnMessageReceived -= UpdateHistoryWithOllamaMessage;
        }
    }
}