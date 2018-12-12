using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class LoginButton : MonoBehaviour {

    public TMP_InputField usernameField;
    public TMP_InputField passwordField;

    public void login()
    {
        FindObjectOfType<LoginManagerAndTeleporter>().makeLogin(usernameField.text, passwordField.text);
    }
}
