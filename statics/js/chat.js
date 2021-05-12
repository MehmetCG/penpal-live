
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
    var messageInput = $('input[name="messagetext"]').val();
    $("#messageBox").trigger('reset');
    
    if (messageInput){
    // Create Ajax Call
      $.ajax({         
        url: "/send_message/"+otheruser,
        data: {'messageText': messageInput},
        dataType: 'json',
        headers: { "X-CSRFToken":'{{csrf_token}}', 'X-Requested-With': 'XMLHttpRequest' },           
        success: function (data) {          
          appendSentMessage(data.message)
          scrollToBottom("messages");
          console.log($("#contact"+otheruser));
          console.log($("#contact"+otheruser).length);
          if ( $("#contact"+otheruser).length > 0 ){
            $("#contact"+otheruser).prependTo("#chatedPeople");
            $("#latest"+otheruser).html(messageInput);
          }else{
            createSentChated(data.message);
          }
          
        }});
      
}});


    
//this part is for getting new data
  var oldID;
 
  function updateMsg() {   
    $.getJSON("/get_message/"+otheruser, function(data){
      if (data.result.messageID > oldID) {   
        var counter = parseInt($("#alert"+data.result.sender).text())
        if (data.result.sender == otheruser){
          appendReceivedMessage(data.result);
        }else{ 
          ++counter;
          $("#alert"+data.result.sender).html(counter);
          $("#alert"+data.result.sender).show();
        };
        if ($("#contact"+data.result.sender).length > 0){
          $("#contact"+data.result.sender).prependTo("#chatedPeople");
          $("#latest"+data.result.sender).html(data.result.messageText);
        }else{
          createReceivedChated(data.result);
        }
        scrollToBottom("messages");
      };
      
      oldID = data.result.messageID;
      setTimeout('updateMsg()', 1000);
    });
};

$.ajaxSetup({ cache: false });
updateMsg();

