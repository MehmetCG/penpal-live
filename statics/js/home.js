
function showFilterResult(profiles) {

  if(profiles.length == 0){
    alert("There is no profile that is matched with your filter!")
  }else{
    $("#profiles").empty()
    window.scrollTo(0,0);

    for (i = 0; i < profiles.length; i++){
      profile = profiles[i]

      if (profile.is_online){
      $("#profiles").append('<div class="container profile-page" id="profile-cards" ><div class="row"><div class="card profile-header"><div class="body"><div class="row"><div class="col-lg-4 col-md-4 col-12"><div class="profile-image float-md-right" style="text-align: center;" > <img src="'
      +profile.image+'" alt="" ><div><h4 class="m-t-0 m-b-0"><strong>'+profile.user+'</strong></h4><a href="/chat/'+profile.user+
      '"><button class="btn btn-primary btn-round btn-simple">Message</button></a></div></div></div><div class="col-lg-8 col-md-8 col-12"><table class="table table-user-information"><tbody><tr><td>Status:</td><td><small class="chat-alert-layout badge badge-success" >Online</small></td></tr><tr><td>Gender, Age:</td><td>'
      +profile.gender+', '+profile.age+'</td></tr><tr><td>Country:</td><td>'+profile.country+'</td></tr><td>Native Language:</td><td>'+profile.nativeLanguage+'</td></tr><tr><td>Practising Language:</td><td>'
      +profile.practisingLanguage+'</td></tr><tr><td>Description:</td><td>'+profile.description+'</td></tr></tbody></table></div></div></div></div></div></div>')
      }else{
        $("#profiles").append('<div class="container profile-page" id="profile-cards" ><div class="row"><div class="card profile-header"><div class="body"><div class="row"><div class="col-lg-4 col-md-4 col-12"><div class="profile-image float-md-right" style="text-align: center;" > <img src="'
      +profile.image+'" alt="" ><div><h4 class="m-t-0 m-b-0"><strong>'+profile.user+'</strong></h4><a href="/chat/'+profile.user+
      '"><button class="btn btn-primary btn-round btn-simple">Message</button></a></div></div></div><div class="col-lg-8 col-md-8 col-12"><table class="table table-user-information"><tbody><tr><td>Status:</td><td><small class="chat-alert-layout badge badge-danger" >Last Seen</small> : '
      +profile.last_seen+'</td></tr><tr><td>Gender, Age:</td><td>'
      +profile.gender+', '+profile.age+'</td></tr><tr><td>Country:</td><td>'+profile.country+'</td></tr><td>Native Language:</td><td>'+profile.nativeLanguage+'</td></tr><tr><td>Practising Language:</td><td>'
      +profile.practisingLanguage+'</td></tr><tr><td>Description:</td><td>'+profile.description+'</td></tr></tbody></table></div></div></div></div></div></div>')
      
      }}}}



$("#filter").submit(function(e) {
    e.preventDefault();   
    var age1 = $('select[name="age1"]').val();
    var age2 = $('select[name="age2"]').val();
    var gender = $('select[name="gender"]').val();
    var country = $('select[name="country"]').val();
    var nativeLanguage = $('select[name="nativeLanguage"]').val();
    var practisingLanguage = $('select[name="practisingLanguage"]').val();

    
    
    // Create Ajax Call
      $.ajax({         
        url: "/search/",
        data: { 'age1' : age1,
                'age2' : age2,
                'gender' : gender,
                'country' : country,
                'nativeLanguage' : nativeLanguage,
                'practisingLanguage' : practisingLanguage },
        dataType: 'json',
        headers: { "X-CSRFToken":'{{csrf_token}}', 'X-Requested-With': 'XMLHttpRequest' },           
        success: function (data) {
          showFilterResult(data)
        }});
      
});