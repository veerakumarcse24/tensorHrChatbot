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

  getUserReviews() {
    return this.http.get(environment.hrBackend + `get_user_ratings/`).toPromise();
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
    formData.append('fileKey', fileData, fileData.name);
    return this.http.post(environment.hrBackend + `upload_training_data/`, formData).toPromise();
  }

}
