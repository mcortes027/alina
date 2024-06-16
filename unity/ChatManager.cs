
public class ChatManager : MonoBehaviour
{
    public ScrollRect scrollRect;
    public Text chatContent;
    public InputField inputField;

    // Metodo para agregar mensaje al chat
    public void AddMessage()
    {
        if (!string.IsNullOrEmpty(inputField.text))
        {
            chatContent.text += inputField.text + "\n";
            inputField.text = string.Empty;
            StartCoroutine(ScrollToBottom());
        }
    }

    // Corrutina para desplazar el ScrollRect al fondo
    private IEnumerator ScrollToBottom()
    {
        yield return new WaitForEndOfFrame();
        scrollRect.verticalNormalizedPosition = 0f;
    }
}