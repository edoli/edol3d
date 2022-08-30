#version 330
out vec4 FragColor;
in vec3 WorldPos;

uniform samplerCube environmentMap;
uniform float envscaler;

void main()
{
	vec3 envColor = textureLod(environmentMap, WorldPos, 0.0).rgb;

	FragColor = envscaler * vec4(envColor, 1.0);
}