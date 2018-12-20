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
    [SerializeField]
    private GameObject setPasilloNv2;
    [SerializeField]
    private GameObject pasilloNv1;

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
        client.Post(new System.Uri("http://127.0.0.1:8000/authentication/login/"), new StringContent("{\"username\":\""+username+"\", \"password\":\""+password+"\"}", System.Text.Encoding.UTF8, "application/json"), HttpCompletionOption.AllResponseContent, receiveLogin);
    }

    private void refreshRooms(Voting[] votings)
    {
        var etsiiInterior = GameObject.Find("ETSII_Interior");
        Vector3 rightSideLv2Position = new Vector3(-0.23579f, 0.00732f, -0.201f);
        Vector3 leftSideLv2Position = new Vector3(0.24123f, 0.00732f, -0.201f);
        Vector3 leftSideLv1Position = new Vector3(0.1093345f, 0f, 0.04105011f);
        Vector3 rightSideLv1Position = new Vector3(-0.1106655f, 0f, 0.04105011f);
        float horizontalDistance = 0.26259f;
        float longitudinalDistance = 0.2751f;
        Debug.Log(votings[0].name);
        bool isRightOrLeft = false;
        int distanceFromCenter = 0;
        PasilloController isRoomRightOrLeft = null;
        foreach (var item in votings)
        {
            if (isRoomRightOrLeft == null)
            {
                var pasillo = Instantiate(pasilloNv1, etsiiInterior.transform);
                var pasillo2 = Instantiate(setPasilloNv2, etsiiInterior.transform);
                pasillo2.transform.localScale = new Vector3(1, 1, 1);
                pasillo.transform.localScale = new Vector3(isRightOrLeft ? 1 : -1, 1, 1);
                if (isRightOrLeft)
                {
                    pasillo.transform.localPosition = new Vector3(rightSideLv1Position.x - horizontalDistance * distanceFromCenter, rightSideLv1Position.y, rightSideLv1Position.z);
                    pasillo2.transform.localPosition = new Vector3(rightSideLv2Position.x - horizontalDistance * distanceFromCenter, rightSideLv2Position.y, rightSideLv2Position.z);
                    distanceFromCenter += 1;
                }
                else
                {
                    pasillo.transform.localPosition = new Vector3(leftSideLv1Position.x + horizontalDistance * distanceFromCenter, leftSideLv1Position.y, leftSideLv1Position.z);
                    pasillo2.transform.localPosition = new Vector3(leftSideLv2Position.x + horizontalDistance * distanceFromCenter, leftSideLv2Position.y, leftSideLv2Position.z);
                }
                isRightOrLeft = !isRightOrLeft;
                isRoomRightOrLeft = pasillo2.GetComponent<PasilloController>();
                isRoomRightOrLeft.textoDcha = "Votación:\n"+item.name;
                isRoomRightOrLeft.votableDcha = true;
            }
            else
            {
                isRoomRightOrLeft.textoIzda = "Votación:\n" + item.name;
                isRoomRightOrLeft.votableIzda = true;
                isRoomRightOrLeft = null;
            }

        }
    }

    public void getVotings()
    {
        client.Get(new Uri("http://127.0.0.1:8000/voting/"), HttpCompletionOption.AllResponseContent, r => {
            refreshRooms(JsonHelper.FromJson<Voting>("{\"Items\":"+r.ReadAsString()+"}"));
        });
    }

    public void makeLogout()
    {
        client.Post(new System.Uri("http://127.0.0.1:8000/authentication/logout/"), new StringContent("", System.Text.Encoding.UTF8, "application/json"), HttpCompletionOption.AllResponseContent, null);
        token = null;
    }

    private void commenceProcess(GameObject player)
    {
        //FindObjectOfType<FocusTogglerAndPauser>().canAlternateNormally = false;
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

public static class JsonHelper
{

    public static T[] FromJson<T>(string json)
    {
        Wrapper<T> wrapper = UnityEngine.JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    public static string ToJson<T>(T[] array)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return UnityEngine.JsonUtility.ToJson(wrapper);
    }

    [Serializable]
    private class Wrapper<T>
    {
        public T[] Items;
    }
}