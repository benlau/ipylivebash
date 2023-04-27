// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { LogViewModel } from '..';

describe('LogViewModel', () => {
  test('should be createable', () => {
    const model = createTestModel(LogViewModel);
    expect(model).toBeInstanceOf(LogViewModel);
    expect(model.get('messages')).toEqual([]);
  });

  test('should be createable with a value', () => {
    const state = { messages: [0, 'Foo Bar!'] };
    const model = createTestModel(LogViewModel, state);
    expect(model).toBeInstanceOf(LogViewModel);
    expect(model.get('messages')).toEqual([0, 'Foo Bar!']);
  });
});
