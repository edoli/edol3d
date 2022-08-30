#version 330
layout(location = 0) in vec3 position;

uniform mat4 u_view;
uniform mat4 u_project;

out vec3 WorldPos;

void main()
{
	WorldPos = position;

	mat4 rotView = mat4(mat3(u_view));
	vec4 clipPos = u_project * rotView * vec4(WorldPos, 1.0);

	// gl_Position = clipPos.xyww;

    vec4 view_pos_h = u_view * vec4(position, 1.0);
    vec4 project_pos_h = u_project * view_pos_h;
    gl_Position = project_pos_h;
}