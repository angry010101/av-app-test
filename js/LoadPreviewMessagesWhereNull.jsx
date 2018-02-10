import MessagesStore from 'js/backend/im/MessagesStore.jsx'
import UsersStore from 'js/backend/im/UsersStore.jsx'


const request = require('superagent');

var startedLoadingMorePrev = false;
window.prevOffset = 0
export function startLoadingPreviewMessages(){    
          if (startedLoadingMorePrev) return ;

          startedLoadingMorePrev = true;

          request.get('/execute')
            .set('Content-Type', 'application/x-www-form-urlencoded')
            .query({dialogsOffset: window.prevOffset})
            .end(function(err, res){
              if (err || !res.ok) {
                 alert('Oh no! error');
              } else {
				//Зачастую всё хорошо, но иногда приходит null и скрипт выбивает ошибку именно в следующей строке
				var j = JSON.parse(res.text);
				
                 let c = j.msgs.splice(0,1);
                 UsersStore.add(j.users);
				 UsersStore.addGroups(j.groups);
                 if (window.prevOffset == 0 ){
					 window.lastMsgId = j.msgs[0].mid;
                    UsersStore.setMe(j.me);
                 }
                 MessagesStore.addPrevMessages(j.msgs,j.users,j.groups,c,0);
                 startedLoadingMorePrev = false;
                 window.prevOffset += 20;
              }
            });
}
