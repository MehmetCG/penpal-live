
function scrollToBottom (id) {
  var div = document.getElementById(id);
  if (div){
    div.scrollTop = div.scrollHeight - div.clientHeight};
}

function showchatedPeople (){
  if ($("#name-section").length == 0 ){
    $("#sidepanel").show()
  }
}

function auto_grow(element) {
  element.style.height = "5px";
  element.style.height = (element.scrollHeight)+"px";
}

showchatedPeople() // to show side panel which is hiden on small screens

function appendSentMessage(message) {     
  $("#chats").append('<li class="replies" id="replies"><div class="img-block"><img src="'
  +message.image+'" alt="" /></div><div class="msgbox"><p>'+ message.messageText +'</p><small class="timeBlock">'
  +message.created+'</small></div></li>')}


function appendReceivedMessage(message) {       
  $("#chats").append('<li class="sent"><div class="img-block"><img src="'
  +message.image+'" alt="" /></div><div class="msgbox"><p>'+ message.messageText +'</p><small class="timeBlock">'
  +message.created+'</small></div></li>')}


//create a new line on chated people section when the first message is sent
function createSentChated(message) {       
  $("#chatedPeople").prepend('<li class="contact" id="contact'+message.recipient+'" style="background-color: #eaeef3;"><a href="/chat/'
  +message.recipient+'"><div class="wrap"><div class="img-block"></span><img src="'+message.image+'" alt="" /></div><div class="meta"><h5 class="name bold my-0 text-primary">'
  +message.recipient+'</h5><p class="preview" id="latest'+message.recipient+'">'+message.messageText+'</p></div></div></li></a>')}

//create a new line on chated people section when the first message is received
function createReceivedChated(message) {       
  $("#chatedPeople").prepend('<li class="contact" id="contact'+message.sender+'"><a href="/chat/'+message.sender+'"><div class="wrap"><div class="img-block"></span><img src="'
  +message.image+'" alt="" /></div><div class="meta"><h5 class="name bold my-0 text-primary">'+message.sender+'</h5><p class="preview" id="latest'+message.sender+'">'
  +message.messageText+'</p></div><small id = "alert'+message.sender+'" class="chat-alert badge badge-success">1</small></div></li></a>')}




scrollToBottom("messages");


var current_url = window.location.href
var otheruser = current_url.split("/")[4]

//this part is for sending new message
$("#messageBox").submit(function(e) {
    e.preventDefault();   
    var messageInput = $('textarea[name="messagetext"]').val();
    $("#messageBox").trigger('reset');
    
    if (messageInput){
    // Create Ajax Call
      $.ajax({         
        url: "/send_message/"+otheruser,
        data: {'messageText': messageInput},
        dataType: 'json',
        headers: { "X-CSRFToken":'{{csrf_token}}', 'X-Requested-With': 'XMLHttpRequest' },           
        success: function (data) {          
          appendSentMessage(data)
          scrollToBottom("messages");
          if ( $("#contact"+otheruser).length > 0 ){
            $("#contact"+otheruser).prependTo("#chatedPeople");
            $("#latest"+otheruser).html(messageInput);
          }else{
            createSentChated(data);
          }
          
        }});
      
}});


    
//this part is for getting new data
  var oldID;
 
  function updateMsg() {   
    $.getJSON("/get_message/"+otheruser, function(data){
      if (data.messageID > oldID) {   
        var counter = parseInt($("#alert"+data.sender).text())
        if (data.sender == otheruser){
          appendReceivedMessage(data);
        }else{ 
          ++counter;
          $("#alert"+data.sender).html(counter);
          $("#alert"+data.sender).show();
        };
        if ($("#contact"+data.sender).length > 0){
          $("#contact"+data.sender).prependTo("#chatedPeople");
          $("#latest"+data.sender).html(data.messageText);
        }else{
          createReceivedChated(data);
        }
        scrollToBottom("messages");
      };
      
      oldID = data.messageID;
      setTimeout('updateMsg()', 1000);
    });
};

$.ajaxSetup({ cache: false });
updateMsg();

