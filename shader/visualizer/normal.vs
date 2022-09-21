#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 value;

uniform mat4 u_mvp;

out vec4 vColor;

void main()
{
    gl_Position = u_mvp * vec4(position, 1.0);
	vColor = vec4((value + 1.0) / 2.0, 1.0);
}