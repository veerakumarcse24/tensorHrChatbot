import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Response } from '@angular/http';
@Injectable()
export class ChatService {

  constructor(private http:HttpClient) { }

  converse(chatmsg) {
    return this.http.get(environment.hrBackend + `chat?inputmsg=`+chatmsg).toPromise();
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

}
