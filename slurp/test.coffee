require('source-map-support').install()

elevator = require('./elevator.js');
ns = elevator.new_state

assert_path_when_called_at = (test, state, floor, expected_path) ->
  test.deepEqual(elevator.call(state, floor).path, expected_path)

exports.testElevatorShouldTargetFloorWhenCalled = (test) ->
  assert_path_when_called_at(test, ns(), 1, [1])
  test.done()
