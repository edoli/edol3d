#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 value;

uniform mat4 u_view;
uniform mat4 u_project;

out vec4 vertexColor;

void main()
{
    vec4 view_pos_h = u_view * vec4(position, 1.0);
    vec4 project_pos_h = u_project * view_pos_h;
    gl_Position = project_pos_h;

	vertexColor = vec4(value.rgb, 1.0);
}