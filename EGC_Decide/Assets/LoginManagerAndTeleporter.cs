using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using CI.HttpClient;
using System.Net;
using Newtonsoft.Json;
using System;

public class LoginManagerAndTeleporter : MonoBehaviour {

    [SerializeField]
    private Transform destination;
    private HttpClient client;
    public string token;
    [SerializeField]
    private Transform errorPanel;

	// Use this for initialization
	void Start () {
		client = new HttpClient();
    }
	
	// Update is called once per frame
	void Update () {
		
	}

    public List<Voting> votaciones;

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Player")
        {
            commenceProcess(other.gameObject);
        }
    }

    public void receiveLogin(HttpResponseMessage response)
    {
        Debug.Log("henlo");
        try
        {
            Debug.Log(response.ReadAsString());
            var values = JsonUtility.FromJson<DecideResponse>(response.ReadAsString());
            Debug.Log(values.token);
            this.token = values.token;
            if (token == "" || token == null)
                indicateError("Estas credenciales no son válidas");
            Debug.Log(values.non_field_errors.Count>0?values.non_field_errors[0]:"nada de nada");
        }
        catch (System.ArgumentNullException)
        {
            indicateError("El servidor no está activo en este momento");
        }
        catch (System.Exception e)
        {
            Debug.Log(e);
        }
    }

    private void indicateError(string error)
    {
        StartCoroutine(indicateErrorCoroutine(error, 2));
    }

    private void indicateError(string error, float time)
    {
        StartCoroutine(indicateErrorCoroutine(error, time));
    }

    private IEnumerator indicateErrorCoroutine(string error, float time)
    {
        FindObjectOfType<FocusTogglerAndPauser>().canAlternateNormally = false;
        FindObjectOfType<FocusTogglerAndPauser>().hasFocus = false;
        errorPanel.gameObject.SetActive(true);
        errorPanel.Find("Text").GetComponent<UnityEngine.UI.Text>().text = error;
        yield return new WaitForSecondsRealtime(time);
        errorPanel.gameObject.SetActive(false);
        FindObjectOfType<FocusTogglerAndPauser>().canAlternateNormally = true;
        FindObjectOfType<FocusTogglerAndPauser>().hasFocus = true;
    }

    public void makeLogin(string username, string password)
    {
        Debug.Log("henlo " + username + " " + password);
        client.Post(new System.Uri("http://127.0.0.1:8000/authentication/login/"), new StringContent("{\"username\":\""+username+"\", \"password\":\""+password+"\"}", System.Text.Encoding.UTF8, "application/json"), HttpCompletionOption.AllResponseContent, receiveLogin);
    }

    public void makeLogout()
    {
        client.Post(new System.Uri("http://127.0.0.1:8000/authentication/logout/"), new StringContent("", System.Text.Encoding.UTF8, "application/json"), HttpCompletionOption.AllResponseContent, null);
        token = null;
    }

    private void commenceProcess(GameObject player)
    {
        FindObjectOfType<FocusTogglerAndPauser>().canAlternateNormally = false;
        player.transform.position = destination.position;
    }
}

[System.Serializable]
public class DecideResponse
{
    public string token;
    public List<string> non_field_errors;
}

[System.Serializable]
public class Voting
{
    public int id;
    public string name;
    public string desc;
    public List<Question> preguntas;
    public DateTime start_date;
    public DateTime end_date;
}

[System.Serializable]
public class Question
{
    public string desc;
    public List<string> options;
}