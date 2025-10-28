Here's how to write "Hello, World!" in C#, C, and C++:

---

### C#

```csharp
using System; // Required for Console class

public class HelloWorld
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!"); // Prints the string to the console
    }
}
```

**Explanation:**
*   `using System;`: Imports the `System` namespace, which contains fundamental classes like `Console`.
*   `public class HelloWorld`: Defines a class named `HelloWorld`. In C#, all executable code resides within classes.
*   `public static void Main(string[] args)`: This is the entry point of the C# application.
    *   `public`: The method is accessible from anywhere.
    *   `static`: The method belongs to the class itself, not to an instance of the class.
    *   `void`: The method does not return any value.
    *   `Main`: The conventional name for the entry point method.
    *   `string[] args`: Allows command-line arguments to be passed to the program.
*   `Console.WriteLine("Hello, World!");`: This line uses the `WriteLine` method from the `Console` class (part of the `System` namespace) to print the string "Hello, World!" followed by a new line to the console.

---

### C

```c
#include <stdio.h> // Required for printf function

int main()
{
    printf("Hello, World!\n"); // Prints the string to the console
    return 0; // Indicates successful execution
}
```

**Explanation:**
*   `#include <stdio.h>`: Includes the standard input/output library, which provides functions like `printf`.
*   `int main()`: This is the entry point of the C program.
    *   `int`: Specifies that the `main` function will return an integer value (typically 0 for success).
*   `printf("Hello, World!\n");`: This function from `stdio.h` prints the string "Hello, World!" to the standard output. The `\n` is an escape sequence that represents a newline character, moving the cursor to the next line after printing.
*   `return 0;`: Returns 0 to the operating system, indicating that the program executed successfully.

---

### C++

```cpp
#include <iostream> // Required for std::cout and std::endl

int main()
{
    std::cout << "Hello, World!" << std::endl; // Prints the string to the console
    return 0; // Indicates successful execution
}
```

**Explanation:**
*   `#include <iostream>`: Includes the input/output stream library, which provides objects like `std::cout` and `std::endl`.
*   `int main()`: This is the entry point of the C++ program, similar to C.
*   `std::cout`: This is an object from the `iostream` library used to output data to the console (standard output stream). `std::` indicates that `cout` belongs to the `std` (standard) namespace.
*   `<<`: This is the stream insertion operator, used to send data to the `cout` object.
*   `"Hello, World!"`: The string literal to be printed.
*   `std::endl`: This is a manipulator that inserts a newline character and then flushes the output buffer, ensuring the text appears immediately on the console.
*   `return 0;`: Returns 0 to the operating system, indicating successful program execution.