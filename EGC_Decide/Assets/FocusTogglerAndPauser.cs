using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityStandardAssets.Characters.FirstPerson;

public class FocusTogglerAndPauser : MonoBehaviour {
    private bool focus = true;
    private LoginManagerAndTeleporter loginManager;
    private bool loggedIn
    {
        get
        {
            return loginManager.token != null && loginManager.token != "";
        }
    }
    public bool uiSourcedPause = false;
    public bool canAlternateNormally = true;
    public bool pausesOnFocus = true;
    public bool canvasEnabled
    {
        set
        {
            canvasTarget.gameObject.SetActive(value);
        }
    }
    [SerializeField]
    private Transform canvas;
    [SerializeField]
    private Transform canvas2;
    private Transform canvasTarget
    {
        get
        {
            if (loggedIn)
                canvas.gameObject.SetActive(false);
            else
                canvas2.gameObject.SetActive(false);
            return loggedIn ? canvas2 : canvas;
        }
    }
    public bool hasFocus
    {
        get
        {
            return focus;
        }
        set
        {
            if (focus != value) {
                alternateFocus(value);
            }
        }
    }

    private void alternateFocus(bool value)
    {
        gameObject.GetComponent<CharacterController>().enabled = value;
        gameObject.GetComponent<FirstPersonController>().enabled = value;
        Cursor.lockState = value ? CursorLockMode.Locked : CursorLockMode.None;
        Cursor.visible = !value;
        focus = value;
        canvasEnabled = !value;
    }

	// Use this for initialization
	void Start () {
        Cursor.lockState = CursorLockMode.None;
        loginManager = FindObjectOfType<LoginManagerAndTeleporter>();
    }
	
	// Update is called once per frame
	void Update () {
        if (canAlternateNormally)
        {
            if(pausesOnFocus)
                Time.timeScale = uiSourcedPause ? 0 : 1 - Input.GetAxisRaw("Fire2");
            if (Input.GetAxisRaw("Fire2") > 0.5 || uiSourcedPause)
                hasFocus = false;
            else
                hasFocus = true;
        }
	}
}
