import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Response } from '@angular/http';
import {Observable} from 'rxjs/Rx';
@Injectable()
export class ChatService {

  constructor(private http:HttpClient) { }

  converse(chatmsg) {
    return this.http.get(environment.hrBackend + `chat?inputmsg=`+chatmsg).toPromise();
  }


 //Get IP Adress using http://freegeoip.net/json/?callback
getIpAddress() {
            const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
            return this.http
              .get('http://freegeoip.net/json/?callback',
              { headers: headers })
              .map(response => response || {})
              .catch(this.handleError);
          }

  private handleError(error: HttpErrorResponse):
      Observable<any> {
        //Log error in the browser console
        console.error('observable error: ', error);

        return Observable.throw(error);
    }

  getUserReviews() {
    return this.http.get(environment.hrBackend + `get_user_ratings/`).toPromise();
  }

  clearHistory() {
    return this.http.get(environment.hrBackend + `clear_history/`).toPromise();
  }

  restartServer() {
    return this.http.get(environment.hrBackend + `restart_server/`).toPromise();
  }

  saveRatings(ratingData) {
    return this.http.post(environment.hrBackend + `save_ratings/`, ratingData).toPromise();
  }

  downloadChat() {
    window.location.href = environment.hrBackend + `download_chat/`;
  }

  downloadLogs() {
    window.location.href = environment.hrBackend + `download_logs/`;
  }

  downloadTraingData() {
    window.location.href = environment.hrBackend + `download_training_data/`;
  }

  uploadTrainData(fileData) {
    const formData: FormData = new FormData();
    formData.append('file', fileData, fileData.name);
    console.log(formData)
    return this.http.post(environment.hrBackend + `upload_training_data/`, formData).toPromise();
  }

  trainData() {
    return this.http.get(environment.hrBackend + `trainData/`).toPromise();
  }


}
