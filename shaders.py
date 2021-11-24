vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vex3 inColor;

out vec3 outColor;

void main()
{
    gl_Position = vec4 (position.x, position.y, position.z, 1.0);
    outColor = inColor;
}

"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 

void main()
{
    fragColor = vec4(outColor, 1);
}
"""