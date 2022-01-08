import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';
import '../css/widget.css';

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

export class LogView extends DOMWidgetView {
  views: any = {};
  status = '';

  render() {
    const container = document.createElement('div');
    const content = document.createElement('div');
    const messageView = document.createElement('div');
    const statusHeader = document.createElement('div');

    const statusView = document.createElement('div');

    const loadingSpinner = document.createElement('div');

    this.el.classList.add('livebash-log-view');

    container.classList.add('livebash-log-view-container');
    this.el.appendChild(container);

    loadingSpinner.innerHTML = '<div></div><div></div><div></div><div></div>';
    this.el.appendChild(loadingSpinner);

    content.setAttribute('tabIndex', '1');
    container.appendChild(content);

    content.appendChild(messageView);
    content.appendChild(statusHeader);

    statusHeader.classList.add('livebash-log-view-divider');
    content.appendChild(statusView);

    this.views = {
      messageView,
      statusHeader,
      statusView,
      container,
      loadingSpinner,
      content,
    };

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
    const messages = value.slice(1);
    messages.forEach((line: any) => {
      const elem = document.createElement('p');
      const text = document.createTextNode(line);
      elem.appendChild(text);
      this.views.messageView.appendChild(elem);
    });

    this.scrollToEnd();
  }

  statusHeaderChanged() {
    const value = this.model.get('status_header');
    this.views.statusHeader.textContent = value;
  }

  scrollToEnd() {
    const { container, content } = this.views;
    container.scrollTop = content.scrollHeight;
  }

  statusChanged() {
    const value = this.model.get('status');
    this.views.statusView.textContent = '';

    value
      .map((line: any) => {
        const item = document.createElement('div');
        const text = document.createTextNode(line);
        item.appendChild(text);
        return item;
      })
      .forEach((item: any) => {
        this.views.statusView.appendChild(item);
      });
  }

  heightChanged() {
    const value = this.model.get('height');
    if (value > 0) {
      const height = `${value * 1.2}em`;
      const styles = {
        maxHeight: height,
        height,
      };
      Object.assign(this.views.container.style, styles);
    }
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
    const className = 'livebash-lds';

    if (value) {
      this.views.loadingSpinner.classList.add(className);
    } else {
      this.views.loadingSpinner.classList.remove(className);
    }
  }
}
