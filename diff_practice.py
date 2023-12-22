import taichi as ti
ti.init()

dt = 1e-2
g = -10
t = ti.field(dtype=ti.f32, shape=())
target = 10
# x = ti.field(dtype=ti.f32, shape=(), needs_grad=True)
#theta = ti.field(dtype=ti.f32, shape=(), needs_grad=True)
v0 = ti.field(dtype=ti.f32, shape=(), needs_grad=True)
loss_x = ti.field(dtype=ti.f32, shape=(), needs_grad=True)

@ti.kernel
def substep():
    #x[None] += v0[None] * dt
    #x[None][1] += (v0[None] * ti.sin(theta[None]) + g * t[None]) * dt
    loss_x[None] = target - v0[None] * 10
    t[None] += dt
@ti.kernel
def init():
    t[None] = 0
    #x[None] = 0
    #v[None] = [v0[None] * ti.cos(theta[None]), v0[None] * ti.sin(theta[None])]

# Set the `grad` of the output variables to `1` before calling `func.grad()`.
loss_x.grad[None] = 1
#theta[None] = 0.3 * ti.math.pi
v0[None] = 5
lr = 1e-1
init()
# learning
init()
substep()
substep.grad()
print(v0.grad[None])
    

