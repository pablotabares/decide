using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PasilloController : MonoBehaviour {

    [SerializeField]
    private TextMeshPro cartelIzda;
    [SerializeField]
    private TextMeshPro cartelDcha;
    [SerializeField]
    private GameObject puertaDcha;
    [SerializeField]
    private GameObject puertaIzda;
    public string textoIzda
    {
        set
        {
            cartelIzda.text = value;
        }
    }
    public string textoDcha
    {
        set
        {
            cartelDcha.text = value;
        }
    }
    public bool votableIzda
    {
        set
        {
            puertaIzda.SetActive(!value);
        }
    }
    public bool votableDcha
    {
        set
        {
            puertaDcha.SetActive(!value);
        }
    }


    // Use this for initialization
    void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
