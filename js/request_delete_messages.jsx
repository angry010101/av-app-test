
import dispatcher from "js/backend/Dispatcher.jsx"
const request = require('superagent');

export function deleteDialog(dlgid,dlgtype){
  var str = "Do you really want to delete the dialog";
  var y = confirm(str);
  if (y){
      request.post('/deleteDialog')
            .set('Content-Type', 'application/x-www-form-urlencoded')
            .send({ id: dlgid})
            .end((err, res) => {
              if (err || !res.ok) {
                 alert('Oh no! error');
              } else {
                 window.res = res;
                 var j = JSON.parse(res.text);
                 alert("Dialog has been deleted");
            }}); 
  } 
}


//this.state.uid = peer_id 
//type присутствует но неиспользуется 
deleteDialog(this.state.uid,this.type);
