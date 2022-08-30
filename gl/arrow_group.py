from matplotlib.pyplot import axis
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import ShaderProgram

vertex_shader_code = '''
#version 330 core
layout (location = 0) in vec3 aPos;
uniform mat4 MVP;
void main()
{
   gl_Position = MVP * vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
'''
fragment_shader_code = '''
#version 330 core
out vec4 FragColor;
uniform vec3 color;
void main()
{
   FragColor = vec4(color, 1.0f);
}
'''

class ArrowGroup():
    shader = None

    def __init__(self, position: np.ndarray, direction: np.ndarray):

        assert position.dtype == np.float32
        assert direction.dtype == np.float32
        assert position.shape == direction.shape

        if ArrowGroup.shader is None:
            

        vertices = np.concatenate([
            position, position + direction
        ], axis=0)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.dtype.itemsize * 3, ctypes.c_void_p(0))
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        glUseProgram(shaderProgram);
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "MVP"), 1, GL_FALSE, &MVP[0][0]);
        glUniform3fv(glGetUniformLocation(shaderProgram, "color"), 1, &lineColor[0]);

        glBindVertexArray(self.vao);
        glDrawArrays(GL_LINES, 0, 2);

    def __del__(self):
        glDeleteVertexArrays(1, self.vao);
        glDeleteBuffers(1, self.vbo);
        glDeleteProgram(shaderProgram);

class Line {
    int shaderProgram;
    unsigned int VBO, VAO;
    vector<float> vertices;
    vec3 startPoint;
    vec3 endPoint;
    mat4 MVP;
    vec3 lineColor;
public:
    Line(vec3 start, vec3 end) {

        startPoint = start;
        endPoint = end;
        lineColor = vec3(1,1,1);
        MVP = mat4(1.0f);

        const char *vertexShaderSource = "#version 330 core\n"
            "layout (location = 0) in vec3 aPos;\n"
            "uniform mat4 MVP;\n"
            "void main()\n"
            "{\n"
            "   gl_Position = MVP * vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
            "}\0";
        const char *fragmentShaderSource = "#version 330 core\n"
            "out vec4 FragColor;\n"
            "uniform vec3 color;\n"
            "void main()\n"
            "{\n"
            "   FragColor = vec4(color, 1.0f);\n"
            "}\n\0";

        // vertex shader
        int vertexShader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
        glCompileShader(vertexShader);
        // check for shader compile errors

        // fragment shader
        int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
        glCompileShader(fragmentShader);
        // check for shader compile errors

        // link shaders
        shaderProgram = glCreateProgram();
        glAttachShader(shaderProgram, vertexShader);
        glAttachShader(shaderProgram, fragmentShader);
        glLinkProgram(shaderProgram);
        // check for linking errors

        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);

        vertices = {
             start.x, start.y, start.z,
             end.x, end.y, end.z,

        };
        
        glGenVertexArrays(1, &VAO);
        glGenBuffers(1, &VBO);
        glBindVertexArray(VAO);

        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices.data(), GL_STATIC_DRAW);

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(0);

        glBindBuffer(GL_ARRAY_BUFFER, 0); 
        glBindVertexArray(0); 

    }

    int setMVP(mat4 mvp) {
        MVP = mvp;
        return 1;
    }

    int setColor(vec3 color) {
        lineColor = color;
        return 1;
    }

    int draw() {
        return 1;
    }

    ~Line() {

        glDeleteVertexArrays(1, &VAO);
        glDeleteBuffers(1, &VBO);
        glDeleteProgram(shaderProgram);
    }
};