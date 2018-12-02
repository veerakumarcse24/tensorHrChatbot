import { Component, OnInit, Input,AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { UtilsService } from '../../services/utils.service';
import { ChatComponent } from '../../agent/chat/chat.component';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
	chatService;
  @ViewChild(ChatComponent) child;
  constructor(private coreService: UtilsService) { }

  ngOnInit() {
  	this.coreService.home = 'chat';
  }

  main_page()
  {
  	this.coreService.home = 'chat';
  }

  download_page()
  {
  	this.coreService.home = 'download';
  }

}
