var key_flag=0;
var key_list=[['W',87,"F",0],
                            ['S',83,"B",0],
                            ['A',65,"L",0],
                            ['D',68,"R",0],
                            ['Q',81,"Q",0],
                            ['E',69,"E",0]];

                var c=document.getElementById("myCanvas");
                var ctx=c.getContext("2d");
                var theImage = new Image(); 

                 
                
            function cnvs_getCoordinates(e)
            {
                
                theImage.src = $("#mapimg").attr( "src");
                var a1=$("#mapps").width()/theImage.width;
                var a2 = $("#mapps").height()/theImage.height;
            x=Math.floor(e.clientX-$("#mapps").offset().left);
            y=Math.floor(e.clientY-$("#mapps").offset().top);

            x=Math.floor(x/a1);
            y=Math.floor(y/a2);
            document.getElementById("xycoordinates").innerHTML="(" + x + "," + y + ")";
            document.getElementById("cross").style.visibility="visible";
            }
            
            function cnvs_clearCoordinates()
            {
                document.getElementById("cross").style.visibility="hidden";
            document.getElementById("xycoordinates").innerHTML="";
            }
        function draw()
            {
                
                //cts.globalCompositeOperation="source-over";
                ctx.strokeStyle="#fdc274";
                ctx.beginPath();
                ctx.moveTo(140,0);
                ctx.lineTo(140,280);						
                ctx.stroke();
                ctx.moveTo(0,140);
                ctx.lineTo(280,140);
                ctx.stroke();
            };

    function dirBtnDown(direction) {
                var url = "requestAddress"
                var request = new XMLHttpRequest();
                
                if(direction=="F")	{$("#btn_F").css({'background-color':'red'});};
                if(direction=="B")	{$("#btn_B").css({'background-color':'red'});};
                if(direction=="L")	{$("#btn_LL").css({'background-color':'red'});};
                if(direction=="R")	{$("#btn_RR").css({'background-color':'red'});};
                if(direction=="Q")	{$("#btn_L").css({'background-color':'red'});};
                if(direction=="E")	{$("#btn_R").css({'background-color':'red'});};
                
                request.open("POST", url);
                request.send(direction);
                
        }
 
        function dirBtnUp() {
                var url = "requestAddress"
                var request = new XMLHttpRequest();
                $(".cBTN").css({'background-color':'rgb(124, 124, 124)'});
                request.open("POST", url);
                request.send("S")
        }


function get_video(url){
var request = new XMLHttpRequest();
request.open("POST", url)
}

$(document).ready(function() {

document.getElementById("cross").style.visibility="hidden";
$("#mapps").click(function(e){
var y=e.pageY-$(this).offset().top;
        var x=e.pageX-$(this).offset().left;
        console.log(x);
        console.log(y);
        });
        
$('#btn_s').click(function() {
//$("#stock").load($('#videoS').value)
urls=$("#videoS").val();
console.log("111")
get_video(urls);
//释放按键时

    $('#video').attr('src', urls); 
    
});

$(document).keyup(function(event){
var code=event.keyCode,i,flag=0;
    for(i=0;i<6;i+=1)
    {
        if(key_list[i][1]==code)
        {
            key_list[i][3]=0;
            
            flag=1;
        };
    };

    if(flag==1)
    {dirBtnUp();};
});
//按下按键时
$(document).keydown(function(event){
    var code=event.keyCode,i,flag=0;

    for(i=0;i<6;i+=1)
    {
        if(key_list[i][1]==code )
        {
            //alert("aaa")
            dirBtnDown(key_list[i][2]);
            break;
        };
    };
});
draw();
});