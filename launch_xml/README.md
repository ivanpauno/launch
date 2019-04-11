# launch_xml

This package provides an abstraction of the XML tree.

## XML front-end mapping rules

### Accessing xml attributes

When having an xml tag like:

```xml
<tag attr='2'/>
```

If the entity `e` is wrapping it, the following two statements would be true:
```python
hasattr(e, 'attr') == True
e.attr == '2'
```

As a general rule, the value of the attribute is returned as an string.
Conversion to `float` or `int` should be explicitly done in the parser method, or in a substitution.
For handling lists, see `Built-in Substitutions` section.

### Accessing XML children that aren't an action or a substitution:

In this xml:

```xml
<executable cmd="ls">
    <env name="a" value="100"/>
    <env name="b" value="stuff"/>
</node>
```

The `env` childs could be accessed like:

```python
len(e.env) == 2
e.env[0].name == 'a'
e.env[0].value == '100'
e.env[1].name == 'b'
e.env[1].value == 'stuff'
```

In these cases, `e.env` is a list of entity, which could be accessed in the same abstract way.

### Accessing XML children that are an action or a substitution:

The entity will keep track of which `children` where accessed or not.
The ones which have never been accessed, will be returned when doing:

```python
e.children
```

This call should be done after all the children that shouldn't be parsed have been accessed.

### Built-in substitutions

`$(list [sep=,] a,b,c,d)`
: Substituted by a python list, splited by the separator that follows `sep=`.
  Default separator is `,`.

`$(int 3)`
: Substituted by a python int.

`$(float 3)`
: Substituted by a python float.

`$(find-pkg pkg-name)`
: Substituted by the path to package installation directory in the local filesystem.
  Forward and backwards slashes will be resolved to the local filesystem convention.
  Substitution will fail if the package cannot be found.

`$(find-exec exec-name)`
: Substituted by the path to the executable in the local filesystem.
  Lookups make use of the PATH environment variable.
  Forward and backwards slashes will be resolved to the local filesystem convention.
  Substitution will fail if the executable cannot be found.

`$(var name)`
: Substituted by the value of the launch configuration variable.
  Substitution will fail if the named argument does not exist.

`$(env env-var [default-value])`
: Substituted by the value of the given environment variable
  Substitution will fail if the variable is not set, unless default values are provided.

`$(dirname)`
: Substituted by the current launch file directory name.
  Substitution will always succeed.
