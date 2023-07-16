import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';
import '../css/widget.css';
import { LiveBashPanelRenderer } from '../webcomp';

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
      session_id: '',
      sessions: '',
      notification_permission_request: false,
      notification_permission: '',
      notification_message: '',
      response: '',
      action: '',
      confirmation_required: false,
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
  renderer?: any;

  render() {
    const panel = document.createElement('div');
    const onEvent = (event: any) => {
      this.onPanelResponse(JSON.stringify(event));
    };

    const onReady = () => {
      const isRunning = this.model.get('running');
      const heightInLines = parseInt(this.model.get('height'));
      const confirmationRequired = this.model.get('confirmation_required');
      const script = this.model.get('script');
      const sessions = this.model.get('sessions');
      const sessionId = this.model.get('session_id');

      //@FIXME - Deprecate setAttribute function
      this.renderer.setAttribute('is-running', isRunning);
      this.renderer.setAttribute('height-in-lines', heightInLines);
      this.renderer.setAttribute('confirmation-required', confirmationRequired);
      this.renderer.setAttribute('script', script);
      this.renderer.setAttribute('sessions', sessions);
      this.renderer.setAttribute('session-id', sessionId);
    };

    this.renderer = new LiveBashPanelRenderer(panel, onEvent, onReady);
    this.renderer.render();

    this.el.appendChild(panel);
    this.panel = panel;
    this.renderer.setAttribute('tabIndex', '1');

    this.heightChanged();
    this.runningChanged();
    this.onConfirmationRequiredChanged();

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
    this.model.on('change:action', this.onActionChanged, this);
    this.model.on(
      'change:confirmation_required',
      this.onConfirmationRequiredChanged,
      this
    );
    this.model.on('change:sessions', this.onSessionsChanged, this);
    this.model.on('change:session_id', this.onSessionIdChanged, this);
  }

  messagesChanged() {
    const value = this.model.get('messages');
    this.renderer.setAttribute(
      'messages',
      value
        .map((v: string) => {
          const str = Number.isInteger(v) ? v.toString() : v;
          return str.replace(/^\s+|\s+$/gm, '');
        })
        .join('\n')
    );
  }

  statusHeaderChanged() {
    const value = this.model.get('status_header');
    this.renderer.setAttribute('status-header', value);
  }

  statusChanged() {
    const value = this.model.get('status');
    this.renderer.setAttribute('status', value.join('\n'));
  }

  heightChanged() {
    const value = this.model.get('height');
    this.renderer.setAttribute('height-in-lines', value);
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
    if (value?.message === undefined) {
      return;
    }
    const notification = new Notification('livebash', {
      body: value.message,
      /* requireInteraction true is not working in Mac */
    });
    notification.onclick = (e) => {
      notification.close();
    };
  }

  runningChanged() {
    const value = this.model.get('running');
    this.renderer.setAttribute('is-running', value);
  }

  onPanelResponse(content: string) {
    const value = {
      id: responseId++,
      content,
    };

    this.model.set('response', JSON.stringify(value));
    this.model.save_changes();
    this.touch();
  }

  onConfirmationRequiredChanged() {
    const value = this.model.get('confirmation_required');
    this.renderer.setAttribute('confirmation-required', value);
  }

  onActionChanged() {
    const value = this.model.get('action');
    this.renderer.setAttribute('action', value);
  }

  onSessionsChanged() {
    const value = this.model.get('sessions');
    this.renderer.setAttribute('sessions', value);
  }

  onSessionIdChanged() {
    const value = this.model.get('session_id');
    this.renderer.setAttribute('session-id', value);
  }
}
