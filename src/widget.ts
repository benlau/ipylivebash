import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';
import '../css/widget.css';
import './webcomp';

export class LogViewModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: LogViewModel.model_name,
      _model_module: LogViewModel.model_module,
      _model_module_version: LogViewModel.model_module_version,
      _view_name: LogViewModel.view_name,
      _view_module: LogViewModel.view_module,
      _view_module_version: LogViewModel.view_module_version,
      messages: [],
      divider_text: '',
      height: 0,
      status: [],
      running: false,
      notification_permission_request: false,
      notification_permission: '',
      notification_message: '',
      response: '',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
  };

  static model_name = 'LogViewModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'LogView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

let responseId = 0;

export class LogView extends DOMWidgetView {
  views: any = {};
  status = '';
  panel: HTMLElement;

  render() {
    const panel = document.createElement('live-bash-panel');
    this.el.appendChild(panel);
    this.panel = panel;
    this.panel.setAttribute('tabIndex', "1");
    this.panel.addEventListener('response', (e: any) => {
      this.onPanelResponse(JSON.stringify(e.detail));
    });

    this.heightChanged();
    this.runningChanged();

    this.model.on('change:messages', this.messagesChanged, this);
    this.model.on('change:status_header', this.statusHeaderChanged, this);
    this.model.on('change:status', this.statusChanged, this);
    this.model.on('change:height', this.heightChanged, this);
    this.model.on('change:running', this.runningChanged, this);
    this.model.on(
      'change:notification_permission_request',
      this.onNotificationPermissionRequestChanged,
      this
    );
    this.model.on(
      'change:notification_message',
      this.onNotificationMessageChanged,
      this
    );
  }

  messagesChanged() {
    const value = this.model.get('messages');
    this.panel.setAttribute('messages', value.join("\n"));
  }

  statusHeaderChanged() {
    const value = this.model.get('status_header');
    this.panel.setAttribute('status-header', value);
  }

  statusChanged() {
    const value = this.model.get('status');
    this.panel.setAttribute('status', value.join("\n"));
  }

  heightChanged() {
    const value = this.model.get('height');
    this.panel.setAttribute('height-in-lines', value);
  }

  onNotificationPermissionRequestChanged() {
    const value = this.model.get('notification_permission_request');
    if (!value) {
      return;
    }
    if (!('Notification' in window)) {
      alert('This browser does not support desktop notification');
      return;
    }

    if (Notification.permission === 'denied') {
      this.model.set('notification_permission', Notification.permission);
      this.model.save_changes();
      return;
    }

    Notification.requestPermission().then((permission) => {
      this.model.set('notification_permission', Notification.permission);
      this.model.save_changes();
    });
  }

  onNotificationMessageChanged() {
    const value = this.model.get('notification_message');
    new Notification('livebash', {
      body: value,
    });
  }

  runningChanged() {
    const value = this.model.get('running');
    this.panel.setAttribute('is-running', value);
  }

  onPanelResponse(content: string) {
    const value = {
      id: responseId++,
      content,
    }

    this.model.set('response', JSON.stringify(value));
    this.model.save_changes();
    this.touch();
  }
}
