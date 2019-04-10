function stringToBytes(str)
{
    var arr = new Array(str.length);

    for (var i = 0; i < str.length; i++)
    {
        arr[i] = str.charCodeAt(i);
    }

    return arr;
};

function bytesToString(arr)
{
    var str = '';

    for (var i = 0; i < arr.length; i++)
    {
        str += String.fromCharCode(arr[i]);
    }

    return str;
};

function decode(data)
{
    try
    {
        var node = parseXml(data).documentElement;

        if (node != null && node.nodeName == 'mxfile')
        {
            var diagrams = node.getElementsByTagName('diagram');

            if (diagrams.length > 0)
            {
                data = getTextContent(diagrams[0]);
            }
        }
    }
    catch (e)
    {
        // ignore
    }

    if (true)
    {
        try
        {
            data = atob(data);
        }
        catch (e)
        {
            console.log(e);
            alert('atob failed: ' + e);

            return;
        }
    }

    if (data.length > 0)
    {
        try
        {
            data = bytesToString(pako.inflateRaw(data));
        }
        catch (e)
        {
            console.log(e);
            alert('inflateRaw failed: ' + e);

            return;
        }
    }

    if (true)
    {
        try
        {
            data = decodeURIComponent(data);
        }
        catch (e)
        {
            console.log(e);
            alert('decodeURIComponent failed: ' + e);

            return;
        }
    }

	if (data.length > 0)
	{
        return data;
    }
};

function parseXml(xml)
{
    if (window.DOMParser)
    {
        var parser = new DOMParser();

        return parser.parseFromString(xml, 'text/xml');
    }
    else
    {
        var result = createXmlDocument();

        result.async = 'false';
        result.loadXML(xml);

        return result;
    }
};

function createXmlDocument()
{
    var doc = null;

    if (document.implementation && document.implementation.createDocument)
    {
        doc = document.implementation.createDocument('', '', null);
    }
    else if (window.ActiveXObject)
    {
        doc = new ActiveXObject('Microsoft.XMLDOM');
    }

    return doc;
};

function decodeFromUri()
{
    try
    {
        document.getElementById('textarea').value = decodeURIComponent(document.getElementById('textarea').value)
    }
	catch (e)
	{
		console.log(e);
		alert('decodeURIComponent failed: ' + e);
    }
};

function getTextContent(node)
{
    return (node != null) ? node[(node.textContent === undefined) ? 'text' : 'textContent'] : '';
};

function normalizeXml()
{
  try
  {
    var str = document.getElementById('textarea').value;
    str = str.replace(/>\s*/g, '>');  // Replace "> " with ">"
    str = str.replace(/\s*</g, '<');  // Replace "< " with "<"
    document.getElementById('textarea').value = str;
  }
  catch (e)
  {
    alert(e.message);
  }
};
