// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { LogViewModel } from '..';

describe('LogViewModel', () => {
  describe('LogViewModel', () => {
    it('should be createable', () => {
      const model = createTestModel(LogViewModel);
      expect(model).toBeInstanceOf(LogViewModel);
      expect(model.get('lines')).toEqual([]);
    });

    it('should be createable with a value', () => {
      const state = { lines: [0, 'Foo Bar!'] };
      const model = createTestModel(LogViewModel, state);
      expect(model).toBeInstanceOf(LogViewModel);
      expect(model.get('lines')).toEqual([0, 'Foo Bar!']);
    });
  });
});
