
var current_url = window.location.href;
var otheruser = current_url.split("/")[4];
var oldID2;

function updateMsgLayout() { 
  $.getJSON("/get_message/"+otheruser, function(data){
    if (data.messageID > oldID2) {   
      var counter2 = parseInt($("#alertlayout").text());
      if (data.sender != otheruser){
        ++counter2;
        $("#alertlayout").html(counter2);
        $("#alertlayout").show();
        $("#alertlayout2").html(counter2);
        $("#alertlayout2").show();
      };   
    };
    oldID2 = data.messageID;
    setTimeout('updateMsgLayout()', 1000);
  });
};

$.ajaxSetup({ cache: false });
updateMsgLayout();