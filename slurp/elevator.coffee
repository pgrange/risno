new_state = (values) -> 
  new_state =
    floor: 0,
    open: false,
    path: []
  for key of values
    new_state[key] = values[key]
  new_state

call = (state, floor) ->
  if floor not in state.path
    state.path.push(floor)
  state

next = (state) ->
  if (nowhere_to_go(state))       then nothing(state)
  else if (should_close(state))   then close(state)
  else if (should_open(state))    then open(state)
  else if (should_go_up(state))   then up(state)
  else if (should_go_down(state)) then down(state)
  else nothing()

nothing = (state) ->
  {cmd: 'NOTHING', state: state}

open = (state) ->
  state.path.shift()
  state.open = true
  {cmd: 'OPEN', state: state}

close = (state) ->
  state.open = false
  {cmd: 'CLOSE', state: state}

up = (state) ->
  state.floor = state.floor + 1
  {cmd: 'UP', state: state}

down = (state) ->
  state.floor = state.floor - 1
  {cmd: 'DOWN', state: state}

should_open = (state) ->
  state.floor == state.path[0]

should_close = (state) ->
  state.open

should_go_up = (state) ->
  state.path[0] > state.floor 

should_go_down = (state) ->
  state.path[0] < state.floor 

nowhere_to_go = (state) ->
  state.path.length == 0

exports.new_state = new_state
exports.call = call
exports.next = next
