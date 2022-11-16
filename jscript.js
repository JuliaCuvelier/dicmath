//Pour télécharger les équations
function doDownload(str) {
    function dataUrl(data) {
        return "data:x-application/xml;charset=utf-8," + escape(data);
    }
    var downloadLink = document.createElement("a");
    downloadLink.href = dataUrl(str);
    downloadLink.download = "feuille.txt";

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

//Pour ajouter des feuilles d'équation
 function add() {

	//Create an input type dynamically.
	var element = document.createElement("textarea");
    
    var nb_eq=countEquations();
    
    //Get id
    var id_area="feuille"+nb_eq;

    //Get label
    name_area="Feuille d'équation "+(nb_eq+1+1); 
    var label_=document.createElement("label");
    label_.setAttribute("value", name_area);
    label_.textContent=name_area;

	//Assign different attributes to the equation sheet.
	element.setAttribute("name", "textarea");
    element.setAttribute("cols",100);
    element.setAttribute("rows",15);
    element.setAttribute("class", "equation");
    element.setAttribute("required",true);
    element.setAttribute("id", id_area);

    //Seaparation
    var hr_=document.createElement("hr")

    //Skip line
    var br_=document.createElement("br");
    
	//Append the element in page.
    var foo = document.getElementById("fooBar");

    foo.appendChild(label_);
    foo.appendChild(br_);
	foo.appendChild(element);
    

    //Download sheet
    var down=document.createElement("button")
    down.textContent= "Télécharger le document";   
    down.setAttribute("onclick",doDownload(element.value));    
    //down.setAttribute(disabled, true);
    foo.appendChild(down);
    down.setAttribute(disabled, false);
    //down.onclick=doDownload(document.getElementById(id_area).value);
    
    foo.appendChild(hr_);
}
function countEquations(){   
    var nb_eq=document.getElementsByClassName("equation").length
    
    return nb_eq;
}
/*document.addEventListener('keydown', function (event) {
    console.log(event.key);
});*/
