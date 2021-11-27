vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;

out vec3 outColor;
out vec2 outTexCoords;

void main()
{
    vec4 pos = vec4 (position.x, position.y, position.z, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
    outColor = vec3(1.0, 1.0, 1.0);
    outTexCoords = texCoords;
}

"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 
in vec2 outTexCoords;

uniform sampler2D tex;

void main()
{
    fragColor = vec4(outColor, 1) * texture(tex, outTexCoords);
}
"""