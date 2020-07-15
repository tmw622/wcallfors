var XMLHttpReq;

function createXMLHttpRequest() {
    if(window.XMLHttpRequest) {
        XMLHttpReq = new XMLHttpRequest();
    }else if (window.ActiveXObject) {
        try
        {
            XMLHttpReq = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                XMLHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {}
        }
    }
}

function SendPost(param,type,url,funcname)
{
    createXMLHttpRequest();
    XMLHttpReq.open(type, url, true);
    XMLHttpReq.onreadystatechange=funcname;

    if(type=="post")
        XMLHttpReq.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    else if (type=="get")
        param=null;

    XMLHttpReq.setRequestHeader("If-Modified-Since","0");
    XMLHttpReq.send(param);
}

function getobject(id)
{
    var obj=document.getElementById(id);
    return obj;
}


function getxforie()
{
    return event.x;
}

function getyforie()
{
    return event.y;
}

function getxforff(event)
{
    return event.clientX;
}

function getyforff(event)
{
    return event.clientY;
}


function checkbrowser()
{
    if (window.navigator.userAgent.indexOf("MSIE")>=1)
        return "ie";
    else if (window.navigator.userAgent.indexOf("Firefox")>=1)
        return "ff";
    else if(window.navigator.userAgent.indexOf("Chrome")>=1)
        return "chrome";
}

function gourl(url)
{
    location.href=url;
}

function CheckBg()
{
   var holder=document.getElementById("bgdiv");
   return holder.style.display;
}

function showbg()
{
    var holder=document.getElementById("bgdiv");
	
    holder.style.width=document.body.clientWidth;
	
    if (document.body.clientHeight>document.body.scrollHeight)
        holder.style.height=document.body.clientHeight;
    else
        holder.style.height=document.body.scrollHeight;

    holder.style.display="block";
}


function showdivbox(title,width,height)
{
    var divbox=getobject("divbox");
    divbox.style.width=width;
    divbox.style.height=height;

    var divtitle=getobject("divtitle");
    divtitle.innerHTML=title;

    return divbox;
}

function redivbox()
{
    var divbox=getobject("divbox");
	var divorgwid=divbox.style.width;
	var divboxwid=divorgwid.substring(0,divorgwid.indexOf("p"));
    divbox.style.left=document.body.clientWidth/2-divboxwid/2;
}

function showfuncbox(title,width,height,src)
{
    showbg();
    var ciframes=getobject("contentframes");

    if(checkbrowser()=="ie")   
        ciframes.style.width=width;
    else
        ciframes.style.width=width-5;
    
    ciframes.style.height=height-50;
    ciframes.src=src;

    var funcbox=showdivbox(title,width,height);
    funcbox.style.left=document.body.clientWidth/2-width/2;
    funcbox.style.top=document.body.clientHeight/2+document.body.scrollTop-height/2;

    funcbox.style.display="block";
}

function disdivbox()
{
    disbg();
    var divbox=getobject("divbox");
    divbox.style.display="none";
	
    var divtitle=getobject("divtitle");
    divtitle.innerHTML="";
	
    var ciframes=getobject("contentframes");
    ciframes.src="";
}

function disbg()
{
    var holder=document.getElementById("bgdiv");
    holder.style.display="none";
}


function goiframes(url)
{
	var frames=getobject("mainiframes");
	frames.src=url;
}

function showtip(objid,event)
{
    var previewdivbox=getobject("tipdiv");
    var linktitle=getobject(objid);
    var  x =linktitle.offsetLeft,y=linktitle.offsetTop;   
    while(linktitle=linktitle.offsetParent)
    {
        x +=linktitle.offsetLeft;   
        y +=linktitle.offsetTop;
    } 
    previewdivbox.style.left=x;
    var posy;
    if(checkbrowser()=="ie")
        posy=getyforie();
    else 
        posy=getyforff(event);
    previewdivbox.style.top=y;
    previewdivbox.style.display="block";
}

function distip()
{
    var previewdivbox=getobject("tipdiv");
    previewdivbox.style.display="none";
}

		   
function clearoption(selectid)
{
    alert(selectid)
    var selobj=getobject(selectid);
    selobj.options.length=0;
}

function addoption(selectid,opttext,optid)
{
    var selobj=getobject(selectid);
    selobj.options.add(new Option(opttext,optid));
}

function GetRandNum(Min,Max)
{
    var Range = Max - Min;
    var Rand = Math.random();
    return(Min + Math.round(Rand * Range));
}


