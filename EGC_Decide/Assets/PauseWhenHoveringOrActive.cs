using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class PauseWhenHoveringOrActive : MonoBehaviour {

    private GameObject focusedUIElement;
    private GameObject selectedUIElement;
    private TMP_InputField inputField;

	// Use this for initialization
	void Start () {
        inputField = gameObject.GetComponent<TMP_InputField>();
    }

    public void addToFocused(GameObject g)
    {
        focusedUIElement = g;
    }

    public void selectThis(GameObject g)
    {
        selectedUIElement = g;
    }

    public void deselectThis(GameObject g)
    {
        selectedUIElement = null;
    }

    public void removeFromFocused(GameObject g)
    {
        focusedUIElement = null;
    }
	
	// Update is called once per frame
	void Update () {
        if (focusedUIElement != null || selectedUIElement != null)
            FindObjectOfType<FocusTogglerAndPauser>().uiSourcedPause = true;
        else
            FindObjectOfType<FocusTogglerAndPauser>().uiSourcedPause = false;
	}
}