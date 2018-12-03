import { Component, OnInit, Input,AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { ChatService } from '../../services/chat.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { trigger,style,transition,animate,keyframes,query,stagger } from '@angular/animations';
import { UtilsService } from '../../services/utils.service';
import { Response } from '@angular/http';
import { HttpClient } from '@angular/common/http';
import {MatSnackBar} from '@angular/material';

@Component({
  // tslint:disable-next-line:component-selector
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
  animations: [

    trigger('listAnimation', [
      transition('* => *', [

        query(':enter', style({ opacity: 0 }), {optional: true}),

        query(':enter', stagger('500ms', [
          animate('.3s ease-in-out', keyframes([
            style({opacity: 0, offset: 0}),
            style({opacity: .5, offset: 0.5}),
            style({opacity: 1,  offset: 1.0}),
          ]))]), {optional: true})
      ])
    ])

  ]
})

export class ChatComponent implements OnInit {
  chatInitial;
  ratingInitial;
  chatCurrent;
  rating;
  ratingClick;
  itemId;
  ratingData;
  username;
  steps;
  comments;
  user_reviews_data;
  
  messages: Message[] = [];
  prettyChatCurrent;

  chatForm: FormGroup;
  chatFormFields: any;
  ratingFields: any;
  @ViewChild('scrollMe') private myScrollContainer: ElementRef;

  constructor(
    public fb: FormBuilder, public chatService: ChatService, private coreService: UtilsService, private http: HttpClient, public snackBar: MatSnackBar) {

    this.chatFormFields = {
      input: [''],
    };
    this.chatForm = this.fb.group(this.chatFormFields);

  }

  ngOnInit() {

    this.clearRatings();
    this.chatInitial = 'hi';

    this.chatService.converse(this.chatInitial)
      .then((c: any) => {
        c.owner = 'chat';
        this.changeCurrent(c);
        this.render_bubbles(c)
      });
  }

  clearRatings(){
    this.steps = 0;
    this.username = '';
    this.rating = 0;
    this.comments = '';
  }

  scrollToBottom(): void {
    try {
        this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
    } catch(err) { }                 
  }

  render_bubbles(c){
    c.speechResponse.forEach((item, index) => {
      if (index  == 0){
          this.add_to_messages(item,"chat")
      }else{
        setTimeout(()=>{
          this.add_to_messages(item,"chat")
        },500)
      }

    });
  }
  add_to_messages(message,author){
      let new_message = new Message(message,author)
      this.messages.push(new_message);
      setTimeout(()=>{
        this.scrollToBottom();
      },300)
      
  }
  
  changeCurrent(c) {
    c.date = new Date();
    this.chatCurrent = c;
    this.prettyChatCurrent = JSON ? JSON.stringify(c, null, '  ') : 'your browser doesnt support JSON so cant pretty print';
  }

  onClick(rating: number): void {
    this.rating = rating;
  }

  submitRating() {
    this.ratingData = {
      'username' : this.username,
      'rating' : this.rating,
      'comments': this.comments
    };
    this.coreService.displayLoader(true);
    this.chatService.saveRatings(this.ratingData)
      .then((c: any) => {
        this.coreService.displayLoader(false);
        this.snackBar.open(c.message, 'Undo', {
          duration: 3000
        });
        this.clearRatings();
      });
  }

  send() {
    const form = this.chatForm.value;
    const sendMessage = {
      ... this.chatCurrent,
      input: form.input,
      owner: 'user'
    };
    this.add_to_messages(form.input,"user")

    this.changeCurrent(sendMessage);
    this.chatService.converse(form.input)
      .then((c: any) => {
        c.owner = 'chat';
        this.changeCurrent(c);
        this.chatForm.reset();
        setTimeout(
          ()=>{
            this.render_bubbles(c);
          },1000
        )
        
      });

  }

  downloadChat() {
    this.chatService.downloadChat();
  }

  downloadLogs() {
    this.chatService.downloadLogs();
  }

  getUserReviews() {
  this.coreService.displayLoader(true);
    this.chatService.getUserReviews()
        .then((c: any) => {
          this.user_reviews_data = c.data;
          if(this.user_reviews_data)
          {
            for(var i=0; i < this.user_reviews_data.length; i++)
            {
              this.user_reviews_data[i].ratingArr = new Array(parseInt(this.user_reviews_data[i].rating));
              console.log(this.user_reviews_data[i]);
            }
          }
          this.coreService.displayLoader(false);
        });
  }

}

export class Message {
  content: string;
  author: string;

  constructor(content: string, author: string){
    this.content = content;
    this.author = author;
  }
}
