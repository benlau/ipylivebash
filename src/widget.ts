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
      lines: [],
      divider_text: '',
      height: 0,
      bottom_text: [],
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
  bottomText = '';

  render() {
    const container = document.createElement('div');
    const topTextView = document.createElement('div');
    const divider = document.createElement('div');
    const bottomTextView = document.createElement('div');

    container.classList.add('livebash-log-view-container');
    container.setAttribute('tabIndex', '1');

    divider.classList.add('livebash-log-view-divider');

    this.el.classList.add('livebash-log-view');
    this.el.appendChild(container);

    container.appendChild(topTextView);
    container.appendChild(divider);
    container.appendChild(bottomTextView);

    this.views = {
      topTextView,
      divider,
      bottomTextView,
      container,
    };

    this.heightChanged();

    this.model.on('change:lines', this.linesChanged, this);
    this.model.on('change:divider_text', this.dividerTextChanged, this);
    this.model.on('change:bottom_text', this.bottomTextChanged, this);
    this.model.on('change:height', this.heightChanged, this);
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

  linesChanged() {
    const value = this.model.get('lines');
    const lines = value.slice(1);
    lines.forEach((line: any) => {
      const elem = document.createElement('p');
      const text = document.createTextNode(line);
      elem.appendChild(text);
      this.views.topTextView.appendChild(elem);
    });

    this.scrollToEnd();
  }

  dividerTextChanged() {
    const value = this.model.get('divider_text');
    this.views.divider.textContent = value;
  }

  scrollToEnd() {
    const { container } = this.views;
    this.el.scrollTop = container.scrollHeight;
  }

  bottomTextChanged() {
    const value = this.model.get('bottom_text');
    this.views.bottomTextView.textContent = '';

    value
      .map((line: any) => {
        const item = document.createElement('div');
        const text = document.createTextNode(line);
        item.appendChild(text);
        return item;
      })
      .forEach((item: any) => {
        this.views.bottomTextView.appendChild(item);
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
}
