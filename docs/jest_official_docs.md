# Jest Official Documentation (Comprehensive)

## 1. Getting Started

To install Jest:
```bash
npm install --save-dev jest
```

## 2. Matchers (Expect)
Jest uses `expect` with various matchers to test values.
- **Exact Equality**: `expect(value).toBe(42)` (uses `Object.is`)
- **Object Equality**: `expect(value).toEqual({a: 1})` (recursive equality for objects/arrays)
- **Truthiness**: `toBeNull()`, `toBeUndefined()`, `toBeDefined()`, `toBeTruthy()`, `toBeFalsy()`
- **Numbers**: `toBeGreaterThan()`, `toBeLessThan()`, `toBeCloseTo()`
- **Strings**: `toMatch(/regex/)`
- **Arrays**: `toContain(item)`
- **Exceptions**: `toThrow(Error)`

```javascript
test('object assignment', () => {
  const data = {one: 1};
  data['two'] = 2;
  expect(data).toEqual({one: 1, two: 2});
});
```

## 3. Testing Asynchronous Code

It is crucial to handle asynchronous tests correctly, otherwise the test will complete before the promise resolves.

### Promises
Return a promise from your test:
```javascript
test('the data is peanut butter', () => {
  return fetchData().then(data => {
    expect(data).toBe('peanut butter');
  });
});
```
If you expect a promise to be rejected, use the `.catch` method. Make sure to add `expect.assertions` to verify that a certain number of assertions are called.
```javascript
test('the fetch fails with an error', () => {
  expect.assertions(1);
  return fetchData().catch(e => expect(e).toMatch('error'));
});
```

### Async / Await
The most common and readable way is using `async` and `await`.
```javascript
test('the data is peanut butter', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});

test('the fetch fails with an error', async () => {
  expect.assertions(1);
  try {
    await fetchData();
  } catch (e) {
    expect(e).toMatch('error');
  }
});
```

### `.resolves` / `.rejects`
You can also combine `async/await` with `.resolves` or `.rejects`.
```javascript
test('the data is peanut butter', async () => {
  await expect(fetchData()).resolves.toBe('peanut butter');
});

test('the fetch fails with an error', async () => {
  await expect(fetchData()).rejects.toMatch('error');
});
```

## 4. Setup and Teardown

If you have work you need to do repeatedly for many tests, you can use `beforeEach` and `afterEach`.
```javascript
beforeEach(() => {
  initializeCityDatabase();
});

afterEach(() => {
  clearCityDatabase();
});

test('city database has Vienna', () => {
  expect(isCity('Vienna')).toBeTruthy();
});
```

If you only need to run setup once before all tests:
```javascript
beforeAll(() => {
  return initializeCityDatabase();
});

afterAll(() => {
  return clearCityDatabase();
});
```

### Scoping with `describe`
You can group tests together using a `describe` block. `beforeEach` and `afterEach` hooks inside a `describe` block only apply to tests within that block.

## 5. Mock Functions

Mock functions allow you to test links between code by erasing actual implementations.

### `jest.fn()`
```javascript
const mockCallback = jest.fn(x => 42 + x);
mockCallback(0);
mockCallback(1);

// Assertions
expect(mockCallback.mock.calls).toHaveLength(2);
expect(mockCallback.mock.calls[0][0]).toBe(0);
expect(mockCallback).toHaveBeenCalledWith(1);
```

### Mock Return Values
```javascript
const myMock = jest.fn();
myMock.mockReturnValueOnce(10).mockReturnValueOnce('x').mockReturnValue(true);
```

### Mocking Promises
When mocking async functions, use `mockResolvedValue` or `mockRejectedValue`.
```javascript
const asyncMock = jest.fn().mockResolvedValue(43);
// Equivalent to: jest.fn().mockImplementation(() => Promise.resolve(43))
```

## 6. Mocking Modules

To mock entire modules, use `jest.mock()`.
```javascript
import axios from 'axios';
import Users from './users';

jest.mock('axios');

test('should fetch users', async () => {
  const users = [{name: 'Bob'}];
  const resp = {data: users};
  axios.get.mockResolvedValue(resp);

  const data = await Users.all();
  expect(data).toEqual(users);
  expect(axios.get).toHaveBeenCalledWith('/users.json');
});
```

## 7. Fake Timers

Native timer functions (i.e., `setTimeout`, `setInterval`, `clearTimeout`, `clearInterval`) are less than ideal for a testing environment since they depend on real time to elapse.

```javascript
// timerGame.js
function timerGame(callback) {
  setTimeout(() => {
    callback();
  }, 1000);
}
```

```javascript
// timerGame.test.js
jest.useFakeTimers();

test('waits 1 second before calling the callback', () => {
  const timerGame = require('./timerGame');
  const callback = jest.fn();

  timerGame(callback);

  // At this point in time, the callback should not have been called yet
  expect(callback).not.toBeCalled();

  // Fast-forward until all timers have been executed
  jest.runAllTimers();

  // Alternatively, advance by specific time:
  // jest.advanceTimersByTime(1000);

  // Now our callback should have been called!
  expect(callback).toBeCalled();
  expect(callback).toHaveBeenCalledTimes(1);
});
```

## 8. Snapshot Testing

Snapshot tests are a very useful tool whenever you want to make sure your UI does not change unexpectedly.
```javascript
import renderer from 'react-test-renderer';
import Link from '../Link';

it('renders correctly', () => {
  const tree = renderer
    .create(<Link page="http://www.facebook.com">Facebook</Link>)
    .toJSON();
  expect(tree).toMatchSnapshot();
});
```
