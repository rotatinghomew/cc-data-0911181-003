from . import routing
from . import course_demand
from . import replies

OPERATIONS={
    'routing.assign':routing.assign,
    'course_demand.confirm':course_demand.confirm,
    'replies.resolve':replies.resolve,
}
